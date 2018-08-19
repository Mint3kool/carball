from replay_analysis.json_parser import Game
from replay_analysis.generated.api import game_pb2
from replay_analysis.generated.api.metadata import game_metadata_pb2
import logging

logger = logging.getLogger(__name__)


class AnalysisManager:

    def create_analysis(self, game: Game):
        logger.info("Creating SaltieGame from %s" % game)
        protobuf_game = game_pb2.Game()
        game_metadata = self.get_game_metadata(game)

    def get_game_metadata(self, game: Game) -> game_metadata_pb2.GameMetadata:
        pass
