from .. import config, factories
from ..components.attack import Attack
from ..components.builder import Builder
from ..components.factory import Factory
from ..components.gatherer import Gatherer
from ..components.movable import Movable
from ..components.player import Player
from ..components.position import Position
from ..components.vision import Vision
from ..game_state import GameState
from ..utils.targeting import Targeting


class AISystem:
    """Controls the behavior of AI-controlled entities."""

    def update(self, game_state: GameState) -> None:
        """Processes AI logic for all entities."""
        # For simplicity, this AI logic is for player 2 only.
        ai_player_id = 2

        # --- AI-level strategic decisions ---
        self._manage_building(game_state, ai_player_id)
        self._manage_production(game_state, ai_player_id)

        # --- Unit-level tactical decisions ---
        for entity_id, components in list(game_state.entities.items()):
            player = components.get(Player)
            if not player or player.is_human or player.player_id != ai_player_id:
                continue

            # Assign idle gatherers to find minerals
            gatherer = components.get(Gatherer)
            if gatherer and not gatherer.target_resource_id:
                vision = components.get(Vision)
                my_pos = components.get(Position)
                if vision and my_pos:
                    closest_minerals = Targeting.find_closest_minerals(
                        entity_id, my_pos, vision, game_state
                    )
                    if closest_minerals:
                        gatherer.target_resource_id = closest_minerals

            # Assign idle combat units to find enemies
            attack = components.get(Attack)
            if attack and not attack.attack_target:
                vision = components.get(Vision)
                my_pos = components.get(Position)
                if vision and my_pos:
                    closest_enemy = Targeting.find_closest_enemy(
                        entity_id, my_pos, player, vision, game_state
                    )
                    if closest_enemy:
                        attack.attack_target = closest_enemy

    def _manage_building(self, game_state: GameState, player_id: int):
        """Decides if and where the AI should build new structures."""
        # Does the AI have a factory?
        has_factory = False
        for components in game_state.entities.values():
            if (
                components.get(Player, {}).player_id == player_id
                and components.get(Factory)
            ):
                has_factory = True
                break

        # If no factory and enough resources, build one.
        if not has_factory:
            factory_cost = config.UNIT_COSTS["unit_factory"]["minerals"]
            if game_state.resources[player_id]["minerals"] >= factory_cost:
                # Find an idle builder
                for builder_id, components in game_state.entities.items():
                    builder = components.get(Builder)
                    player = components.get(Player)
                    if (
                        builder
                        and player
                        and player.player_id == player_id
                        and not builder.build_target
                    ):
                        # Found an idle builder, command it to build.
                        builder_pos = components.get(Position)
                        build_pos = (builder_pos.x + 3, builder_pos.y)

                        game_state.resources[player_id]["minerals"] -= factory_cost
                        factories.create_unit_factory(
                            game_state,
                            build_pos[0],
                            build_pos[1],
                            player_id,
                            is_human=False,
                        )
                        # In this simplified AI, we build instantly.
                        # A more advanced AI would create a build site and wait.
                        break  # Build one factory at a time.

    def _manage_production(self, game_state: GameState, player_id: int):
        """Decides which units to produce from factories."""
        unit_cost = config.UNIT_COSTS["chassis"]["minerals"]
        if game_state.resources[player_id]["minerals"] >= unit_cost:
            # Find a factory with an empty queue
            for entity_id, components in game_state.entities.items():
                factory = components.get(Factory)
                player = components.get(Player)
                if (
                    factory
                    and player
                    and player.player_id == player_id
                    and not factory.production_queue
                ):
                    # Queue a new chassis
                    game_state.resources[player_id]["minerals"] -= unit_cost
                    factory.production_queue.append("chassis")
                    break  # Queue one unit at a time.