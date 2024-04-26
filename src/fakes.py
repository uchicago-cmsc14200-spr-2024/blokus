"""
Fake implementations of BlokusBase.

We provide a BlokusStub implementation, and
you must provide a BlokusFake implementation.
"""
from shape_definitions import ShapeKind
from piece import Point, Shape, Piece
from base import BlokusBase, Grid


class BlokusStub(BlokusBase):
    """
    Stub implementation of BlokusBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players.
    - Only three of the 21 Blokus shapes are available:
      the one-square, two-square, and three-square straight pieces.
    - Players are allowed to place pieces in any position of the board
      they want, even if the piece collides with any squares of
      previously played pieces (squares of the new piece replace any
      conflicting ones).
    - Board positions are not validated. If a method is called with
      a position outside the board, it will likely cause an exception.
    - There is no consideration of start positions for a player's
      first move.
    - The constructor simulates two initial moves: placing
      Player 1's "1" piece in the top-left corner and
      Player 2's "2" piece in the bottom-right corner.
    - The game ends after six moves. The player, if any, who has a
      piece occupying the top-right corner of the board wins.
      Otherwise, the players tie.
    - The `remaining_shapes` method always says all three shapes remain.
    - The only shape that is considered available by `available_moves`
      is the one-square shape, and it is considered available everywhere
      on the board regardless of whether the corresponding positions are
      available or occupied.
    - Several methods return simple, unhelpful results (as opposed to
      raising NotImplementedErrors).
    """

    _shapes: dict[ShapeKind, Shape]
    _size: int
    _num_players: int
    _curr_player: int
    _grid: Grid
    _num_moves: int

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Constructor (See BlokusBase)

        This stub initializes a counter for number of moves
        in order to implement a simple game_over condition.

        Once everything is initialized, this stub implementation
        "simulates" two moves.
        """
        super().__init__(num_players, size, start_positions)
        self._shapes = self._load_shapes()
        self._size = size
        self._num_players = 2
        self._curr_player = 1
        self._grid = [[None] * size for _ in range(size)]
        self._num_moves = 0
        self._simulate_two_moves()

    def _load_shapes(self) -> dict[ShapeKind, Shape]:
        """
        Rather than reading in the representations of shapes
        from shape_definitions.py, this method manually builds
        three of the 21 kinds of shapes.

        See shape_definitions.py for more details.
        """
        # See shape_definitions.definitions[ShapeKind.ONE]
        shape_1 = Shape(ShapeKind.ONE, (0, 0), False, [(0, 0)])

        # See shape_definitions.definitions[ShapeKind.TWO]
        shape_2 = Shape(ShapeKind.TWO, (0, 0), True, [(0, 0), (0, 1)])

        # See shape_definitions.definitions[ShapeKind.THREE]
        shape_3 = Shape(
            ShapeKind.THREE, (0, 1), True, [(0, -1), (0, 0), (0, 1)]
        )

        return {
            ShapeKind.ONE: shape_1,
            ShapeKind.TWO: shape_2,
            ShapeKind.THREE: shape_3,
        }

    def _simulate_two_moves(self) -> None:
        """
        Simulates two moves:

        - Player 1 places their ShapeKind.ONE piece in the top-left corner.
        - Player 2 places their ShapeKind.TWO piece in the bottom-right corner.

        This drives the game into a state where four more pieces
        can be played before entering the game_over condition
        (six moves total).
        """
        piece_1 = Piece(self.shapes[ShapeKind.ONE])
        piece_1.set_anchor((0, 0))
        self.maybe_place(piece_1)

        # This anchor position accounts for the origin of
        # ShapeKind.TWO as specified in shape_definitions.py.
        piece_2 = Piece(self.shapes[ShapeKind.TWO])
        piece_2.set_anchor((self.size - 1, self.size - 2))
        self.maybe_place(piece_2)

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        See BlokusBase
        """
        return self._shapes

    @property
    def size(self) -> int:
        """
        See BlokusBase
        """
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        """
        See BlokusBase
        """
        return set()

    @property
    def num_players(self) -> int:
        """
        See BlokusBase
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        See BlokusBase
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        See BlokusBase
        """
        return set()

    @property
    def grid(self) -> Grid:
        """
        See BlokusBase
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        See BlokusBase
        """
        return self._num_moves == 6

    @property
    def winners(self) -> list[int]:
        """
        See BlokusBase
        """
        top_right_cell = self.grid[0][self.size - 1]
        if top_right_cell is None:
            return [1, 2]
        else:
            winner = top_right_cell[0]
            return [winner]

    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        See BlokusBase
        """
        return [ShapeKind.ONE, ShapeKind.TWO, ShapeKind.THREE]

    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        return True

    def maybe_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        for r, c in piece.squares():
            self._grid[r][c] = (self.curr_player, piece.shape.kind)
        self._curr_player = (self.curr_player % self.num_players) + 1
        self._num_moves += 1
        return True

    def retire(self) -> None:
        """
        See BlokusBase
        """
        pass

    def get_score(self, player: int) -> int:
        """
        See BlokusBase
        """
        return -999

    def available_moves(self) -> set[Piece]:
        """
        See BlokusBase
        """
        pieces = set()
        for r in range(self.size):
            for c in range(self.size):
                piece = Piece(self.shapes[ShapeKind.ONE])
                piece.set_anchor((r, c))
                pieces.add(piece)

        return pieces


#
# Your BlokusFake implementation goes here
#
