import unittest
import ipywidgets as w
from calmar.widget_lifecycle import close_widget, detach_closed_children
from calmar import widgets as cw


class WidgetLifecycleTests(unittest.TestCase):
    def test_replacing_viewer_does_not_break_old_output_state(self):
        viewer = cw.fresh_viewer('lifecycle-test')
        label = w.HTML('Retained control')
        container = w.VBox([label, viewer])
        replacement = cw.fresh_viewer('lifecycle-test')
        self.addCleanup(close_widget, replacement)
        self.addCleanup(close_widget, label)
        self.addCleanup(close_widget, container)
        self.assertIsNone(viewer.comm)
        self.assertEqual(container.children, (label,))
        self.assertEqual(container.get_state()['children'], ['IPY_MODEL_' + label.model_id])

    def test_live_cleanup_repairs_already_closed_controls_in_nested_boxes(self):
        child, keep = w.Button(description='old'), w.HTML('keep')
        row = w.HBox([child, keep])
        parent = w.VBox([row])
        self.addCleanup(close_widget, parent)
        self.addCleanup(close_widget, row)
        self.addCleanup(close_widget, keep)
        child.close()
        with self.assertRaises(AttributeError):
            row.get_state()
        self.assertGreaterEqual(detach_closed_children(), 1)
        self.assertEqual(row.children, (keep,))
        self.assertEqual(row.get_state()['children'], ['IPY_MODEL_' + keep.model_id])
        self.assertEqual(parent.children, (row,))
