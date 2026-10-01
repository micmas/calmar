"""Palette consistency across overlays, static figures and custom settings."""
import unittest
from calmar import colors


class ColorTests(unittest.TestCase):
    def tearDown(self):
        colors.configure()

    def test_custom_palette_updates_legend_and_plot_hue(self):
        from matplotlib.colors import to_hex
        colors.configure({'manual': 'magenta', 'synthstroke': 'cyan'})
        for source in colors.DEFAULT_MASK_COLORS:
            self.assertEqual(to_hex(colors.cmap(source)(0)), colors.css(source))
            self.assertEqual(to_hex(colors.cmap(source, continuous=True)(1.0)), colors.css(source))
            self.assertIn(colors.color(source), colors.legend([source]))
        self.assertEqual(colors.color('manual'), 'magenta')
        self.assertEqual(colors.color('synthstroke'), 'cyan')

    def test_invalid_setting_does_not_partially_replace_palette(self):
        colors.configure({'manual': 'yellow'})
        for settings in ({'manual': 'not-a-color'}, {'misspelled-origin': 'red'}):
            with self.assertRaises(ValueError):
                colors.configure(settings)
            self.assertEqual(colors.color('manual'), 'yellow')

    def test_binary_palette_can_render_nilearn_roi_and_its_colourbar(self):
        import io
        import matplotlib.pyplot as plt
        import nibabel as nib
        import numpy as np
        from nilearn import plotting
        data = np.zeros((12, 12, 12), dtype=np.uint8)
        data[4:8, 4:8, 4:8] = 1
        mask = nib.Nifti1Image(data, np.eye(4))
        fig = plt.figure()
        try:
            plotting.plot_roi(mask, bg_img=None, cmap=colors.cmap('linda'),
                              figure=fig, colorbar=True, cut_coords=(6, 6, 6))
            output = io.BytesIO()
            fig.savefig(output, format='png')
            self.assertGreater(len(output.getvalue()), 1000)
        finally:
            plt.close(fig)
