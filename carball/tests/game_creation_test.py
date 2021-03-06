import unittest

from carball.analysis.analysis_manager import AnalysisManager

from ..json_parser.game import Game
from ..tests.utils import run_tests_on_list, run_analysis_test_on_replay

from .. import decompile_replays


class DBTest(unittest.TestCase):
    def test_replay_attrs(self):
        local = self

        def test(replay, file_path):
            json_object = decompile_replays.decompile_replay(replay, file_path)
            game = Game()
            game.initialize(loaded_json=json_object)
            info = game.game_info
            local.assertIsNotNone(game.game_info.server_name)
            local.assertIsNotNone(game.map)
            local.assertIsNotNone(game.game_info.match_guid)

        run_tests_on_list(test)

    def test_analysis(self):
        local = self

        def test(analysis: AnalysisManager):
            local.assertIsNotNone(analysis.get_protobuf_data())
            local.assertEqual(False, analysis.get_protobuf_data().game_metadata.is_invalid_analysis)

        run_analysis_test_on_replay(test)

if __name__ == '__main__':
    unittest.main()
