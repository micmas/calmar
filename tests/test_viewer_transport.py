from pathlib import Path
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from ipyniivue.widget import Volume
from ipywidgets.widgets.widget import _remove_buffers

from calmar.viewer_transport import CHUNK_BYTES, LazyVolume, attach_transport, make_lazy, configure_file_server
from calmar.widgets import _DeferredNiiVue
from calmar import widgets as cw
from ipyniivue import NiiVue


class ViewerTransportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)/'image.nii.gz'
        self.data = bytes(range(256)) * (CHUNK_BYTES//256 + 17)
        self.path.write_bytes(self.data)

    def test_restore_contains_descriptors_instead_of_image_buffers(self):
        import numpy as np
        volume = LazyVolume(path=self.path, paired_img_path=self.path)
        self.addCleanup(volume.close)
        volume.img = np.ones((12, 12, 12), dtype=np.float32)
        state, _, buffers = _remove_buffers(volume.get_state())
        self.assertEqual(buffers, [])
        self.assertIsNone(state.get('img'))
        self.assertEqual(volume.img.shape, (12, 12, 12))
        self.assertTrue(state['path']['calmar_lazy'])
        self.assertEqual(state['path']['name'], self.path.name)
        self.assertNotIn(str(self.path.parent), str(state))

    def test_chunks_reconstruct_exact_file_and_reject_unowned_sources(self):
        nv = _DeferredNiiVue()
        self.addCleanup(nv.close)
        nv.load_volumes([dict(path=self.path)])
        self.addCleanup(nv.volumes[0].close)
        nv.send = Mock()
        request = dict(type='calmar:read-volume', request='test', field='path',
                       volume=nv.volumes[0].model_id)
        nv._handle_custom_msg(request, [])
        calls = nv.send.call_args_list
        chunks = [call.kwargs['buffers'][0] for call in calls if 'buffers' in call.kwargs]
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(c) <= CHUNK_BYTES for c in chunks))
        self.assertEqual(b''.join(chunks), self.data)
        self.assertEqual(calls[-1].args[0]['size'], len(self.data))
        for changes in (dict(volume='unowned'), dict(field='/etc/passwd')):
            nv.send.reset_mock()
            nv._handle_custom_msg({**request, **changes}, [])
            self.assertEqual(nv.send.call_count, 1)
            self.assertEqual(nv.send.call_args.args[0]['type'], 'calmar:volume-error')

    def test_http_descriptor_is_versioned_and_only_exposes_served_files(self):
        with patch('calmar.viewer_transport._file_server', None):
            configure_file_server('/user/test/', self.path.parent)
            volume = LazyVolume(path=self.path)
            self.addCleanup(volume.close)
            url = volume.get_state()['path']['url']
            self.assertTrue(url.startswith('/user/test/files/image.nii.gz?v='))
            self.assertNotIn('token', url)
            configure_file_server('/user/test/', self.path.parent / 'other')
            self.assertNotIn('url', volume.get_state()['path'])

    def test_existing_volume_keeps_identity_settings_and_source(self):
        volume = Volume(path=self.path, opacity=.35, colormap='red')
        self.addCleanup(volume.close)
        identity = volume.model_id
        make_lazy(volume)
        self.assertEqual(volume.model_id, identity)
        self.assertEqual(volume.path, self.path)
        self.assertEqual(volume.opacity, .35)
        self.assertEqual(volume.colormap, 'red')
        self.assertEqual(_remove_buffers(volume.get_state())[2], [])

    def test_repeated_attachment_registers_one_handler(self):
        nv = _DeferredNiiVue()
        self.addCleanup(nv.close)
        count = len(nv._msg_callbacks.callbacks)
        attach_transport(nv)
        attach_transport(nv)
        self.assertEqual(len(nv._msg_callbacks.callbacks), count)

    def test_live_upgrade_preserves_models_and_supports_future_volume_changes(self):
        nv = NiiVue()
        self.addCleanup(nv.close)
        nv.load_volumes([dict(path=self.path, opacity=.35)])
        original = nv.volumes[0]
        self.addCleanup(original.close)
        with patch.object(cw, '_VIEWERS', {'old': nv}):
            self.assertEqual(cw.refresh_viewer_frontends(), 1)
            self.assertIs(nv.volumes[0], original)
            self.assertEqual(_remove_buffers(original.get_state())[2], [])
            nv.load_volumes([dict(path=self.path)])
            self.addCleanup(nv.volumes[0].close)
            self.assertEqual(_remove_buffers(nv.volumes[0].get_state())[2], [])

    def test_selection_cache_reuses_layers_but_reloads_replaced_files(self):
        viewer = _DeferredNiiVue()
        self.addCleanup(viewer.close)
        atlas = self.path.with_name('atlas.nii.gz')
        atlas.write_bytes(self.data)
        with patch.multiple(cw, _configured=True, _URL_BASE=False):
            brain = dict(path=self.path, colormap='gray', opacity=1.)
            overlay = dict(path=atlas, opacity=.3)
            cw.set_volumes(viewer, [brain, overlay], cache_size=2)
            first_brain, first_atlas = viewer.volumes
            cw.set_volumes(viewer, [brain], cache_size=2)
            cw.set_volumes(viewer, [brain, overlay], cache_size=2)
            self.assertIs(viewer.volumes[0], first_brain)
            self.assertIs(viewer.volumes[1], first_atlas)
            stamp = atlas.stat().st_mtime_ns
            os.utime(atlas, ns=(stamp + 1, stamp + 1))
            cw.set_volumes(viewer, [brain, overlay], cache_size=2)
            self.assertIs(viewer.volumes[0], first_brain)
            self.assertIsNot(viewer.volumes[1], first_atlas)
            self.assertEqual(len(viewer._calmar_layer_cache), 2)
            self.assertIsNone(first_atlas.comm)
            for model in viewer.volumes:
                self.addCleanup(model.close)

    def test_url_cache_changes_for_an_update_within_the_same_second(self):
        with patch.multiple(cw, _configured=True, _URL_BASE='/test/', _SERVE_ROOT=self.path.parent):
            before = cw.vol(self.path)['url']
            stamp = self.path.stat().st_mtime_ns
            os.utime(self.path, ns=(stamp + 1, stamp + 1))
            self.assertNotEqual(cw.vol(self.path)['url'], before)


if __name__ == '__main__':
    unittest.main()
