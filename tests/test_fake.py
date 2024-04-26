import pytest
from typing import Optional

import shape_definitions
from shape_definitions import ShapeKind
from piece import Shape, Piece
from base import BlokusBase
from fakes import BlokusFake


def test_inheritance() -> None:
    """Test that BlokusFake inherits from BlokusBase"""
    assert issubclass(
        BlokusFake, BlokusBase
    ), "BlokusFake should inherit from BlokusBase"


def init_blokus_mini(num_players: int) -> BlokusBase:
    return BlokusFake(num_players, 5, {(0, 0), (4, 4)})


def init_blokus_mono() -> BlokusBase:
    return BlokusFake(1, 11, {(5, 5)})


def init_blokus_duo() -> BlokusBase:
    return BlokusFake(2, 14, {(4, 4), (9, 9)})


def init_blokus_classic(num_players: int = 2) -> BlokusBase:
    return BlokusFake(num_players, 20, {(0, 0), (0, 19), (19, 0), (19, 19)})


def test_init() -> None:
    """Test that a BlokusFake object is constructed correctly"""
    init_blokus_duo()


def test_init_properties() -> None:
    """Test the properties of a BlokusFake object after it is constructed"""
    blokus = init_blokus_duo()

    assert blokus.size == 14
    assert blokus.num_players == 2
    assert blokus.curr_player == 1
    assert not blokus.game_over


def test_some_shapes_loaded() -> None:
    """Test that (some of the) shapes have been loaded correctly"""
    blokus = init_blokus_duo()

    shape = blokus.shapes[ShapeKind.ONE]
    assert shape.kind == ShapeKind.ONE
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0)]

    shape = blokus.shapes[ShapeKind.LETTER_O]
    assert shape.kind == ShapeKind.LETTER_O
    assert shape.origin == (0, 0)
    assert not shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.Z]
    assert shape.kind == ShapeKind.Z
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 0), (0, 0), (1, 0), (1, 1)]

    shape = blokus.shapes[ShapeKind.V]
    assert shape.kind == ShapeKind.V
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 1), (0, 1), (1, -1), (1, 0), (1, 1)]


def test_shape_five_from_string() -> None:
    """Test that shapes can be loaded using Shape.from_string"""

    shape = Shape.from_string(
        ShapeKind.FIVE, shape_definitions.definitions[ShapeKind.FIVE]
    )
    assert shape.kind == ShapeKind.FIVE
    assert shape.origin == (2, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0)]

    # Test a couple alternative definitions of the FIVE shape

    shape = Shape.from_string(ShapeKind.FIVE, "\nXXOXX")
    assert shape.kind == ShapeKind.FIVE
    assert shape.origin == (0, 2)
    assert shape.can_be_transformed
    assert shape.squares == [(0, -2), (0, -1), (0, 0), (0, 1), (0, 2)]

    shape = Shape.from_string(ShapeKind.FIVE, "\nOXXXX")
    assert shape.kind == ShapeKind.FIVE
    assert shape.origin == (0, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]


def test_shape_u_from_string() -> None:
    """Test that shapes can be loaded using Shape.from_string"""

    shape = Shape.from_string(
        ShapeKind.U, shape_definitions.definitions[ShapeKind.U]
    )
    assert shape.kind == ShapeKind.U
    assert shape.origin == (1, 1)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, -1), (-1, 1), (0, -1), (0, 0), (0, 1)]

    # Test an alternative definition of the U shape

    shape = Shape.from_string(
        ShapeKind.U,
        """
        XX
        O
        XX
        """,
    )
    assert shape.kind == ShapeKind.U
    assert shape.origin == (1, 0)
    assert shape.can_be_transformed
    assert shape.squares == [(-1, 0), (-1, 1), (0, 0), (1, 0), (1, 1)]


def test_wall_collisions() -> None:
    """Test wall collisions with a handful of pieces and empty board"""

    blokus = init_blokus_mini(1)

    # A few shapes for testing
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_five = Piece(blokus.shapes[ShapeKind.FIVE])
    piece_y = Piece(blokus.shapes[ShapeKind.Y])

    # Anchor each of these pieces at every row and column
    for r in range(5):
        for c in range(5):
            piece_one.set_anchor((r, c))
            piece_two.set_anchor((r, c))
            piece_five.set_anchor((r, c))
            piece_y.set_anchor((r, c))

            # ShapeKind.ONE fits everywhere on the board...
            assert not blokus.any_wall_collisions(piece_one)

            # ... but ShapeKind.TWO, FIVE, and Y do not
            if c <= 3:
                assert not blokus.any_wall_collisions(piece_two)
            else:
                assert blokus.any_wall_collisions(piece_two)

            if r == 2:
                assert not blokus.any_wall_collisions(piece_five)
            else:
                assert blokus.any_wall_collisions(piece_five)

            if r in [1, 2] and c >= 1:
                assert not blokus.any_wall_collisions(piece_y)
            else:
                assert blokus.any_wall_collisions(piece_y)

    # As an exercise, refactor the tests above so that
    # _all_ pieces are tested rather than just a handful.
    # And rather than adding separate definitions and if
    # statements for each piece, think about how to check
    # the necessary requirements uniformly for all shapes.
    # What is it about a shape's origin, bounding box, etc.
    # that determine whether there is a wall collision?


def test_place_piece_one() -> None:
    """Test placement of a single piece"""

    blokus = init_blokus_mini(2)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))

    assert blokus.curr_player == 1
    assert blokus.maybe_place(piece_one)
    assert blokus.curr_player == 2
    assert not blokus.game_over


def test_place_pieces_1() -> None:
    """Test placement of two pieces"""

    blokus = init_blokus_mini(2)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))

    # First player plays ONE at (0, 0)
    assert blokus.maybe_place(piece_one)

    # Second player should not be able to play
    # their ONE at the same position
    assert not blokus.maybe_place(piece_one)

    # But they can play it one square over
    piece_one.set_anchor((0, 1))
    assert blokus.maybe_place(piece_one)


def test_place_pieces_2() -> None:
    """Test placement of two pieces"""

    blokus = init_blokus_mini(2)

    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))

    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((0, 0))

    assert blokus.maybe_place(piece_one)

    # Second player cannot play TWO anchored at (0, 0)
    assert blokus.any_collisions(piece_two)
    assert not blokus.maybe_place(piece_two)

    # But they can play it one square over
    piece_two.set_anchor((0, 1))
    assert not blokus.any_collisions(piece_two)
    assert blokus.maybe_place(piece_two)


def test_place_pieces_3() -> None:
    """Test that piece can't be placed in same position"""

    blokus = init_blokus_mini(2)
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])

    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    piece_one.set_anchor((0, 1))
    assert blokus.maybe_place(piece_one)

    # Player 1 has already played ONE
    piece_one.set_anchor((3, 3))
    with pytest.raises(ValueError):
        blokus.maybe_place(piece_one)


def test_retirement_1() -> None:
    """Hmm, retirement..."""

    blokus = init_blokus_duo()

    assert blokus.curr_player == 1
    blokus.retire()

    assert blokus.curr_player == 2
    blokus.retire()

    assert blokus.game_over
    assert blokus.winners == [1, 2]
    assert blokus.get_score(1) == -89
    assert blokus.get_score(2) == -89


def test_retirement_2() -> None:
    """Hmm, retirement..."""

    blokus = init_blokus_duo()

    assert blokus.curr_player == 1
    blokus.retire()

    assert blokus.curr_player == 2
    piece_one = Piece(blokus.shapes[ShapeKind.ONE])
    piece_one.set_anchor((0, 0))
    assert blokus.maybe_place(piece_one)

    assert blokus.curr_player == 2
    piece_two = Piece(blokus.shapes[ShapeKind.TWO])
    piece_two.set_anchor((0, 1))
    assert blokus.maybe_place(piece_two)

    assert blokus.curr_player == 2
    piece_three = Piece(blokus.shapes[ShapeKind.THREE])
    piece_three.set_anchor((0, 4))
    assert blokus.maybe_place(piece_three)

    assert blokus.curr_player == 2
    blokus.retire()

    assert blokus.game_over
    assert blokus.winners == [2]
    assert blokus.get_score(1) == -89
    assert blokus.get_score(2) == -83


def test_grid_x() -> None:
    """
    Test a grid

    In this diagram, we use two characters
    per column to make the board look more
    square. Each 'X' marks a spot of the
    ShapeKind.X piece.

           0 1 2 3 4
         ||||||||||||||
       0 ||          ||
       1 ||    XX    ||
       2 ||  XXXXXX  ||
       3 ||    XX    ||
       4 ||          ||
         ||||||||||||||
    """

    blokus = init_blokus_mini(1)
    piece = Piece(blokus.shapes[ShapeKind.X])
    piece.set_anchor((2, 2))
    assert blokus.maybe_place(piece)

    for r in range(5):
        for c in range(5):
            if (r, c) in [(1, 2), (2, 1), (2, 2), (2, 3), (3, 2)]:
                assert blokus.grid[r][c] == (1, ShapeKind.X)
            else:
                assert blokus.grid[r][c] is None


def test_123457_not_cool() -> None:
    """
    Test grid and score after a few moves

    In this diagram, we use two characters
    per column to make the board look more
    square. Player 1 plays all their "number"
    pieces (ONE, TWO, etc.), and Player plays
    a few "letter" pieces.

                               1
           0 1 2 3 4 5 6 7 8 9 0 1 2 3
         ||||||||||||||||||||||||||||||||
       0 ||                          11||
       1 ||                            ||
       2 ||                            ||
       3 ||              7777  333333  ||
       4 ||        4444444477          ||
       5 ||55              77          ||
       6 ||55                          ||
       7 ||55    CCCC                  ||
       8 ||55    CC  OOOO        LL    ||
       9 ||55        OOOO  OOOO  LL    ||
      10 ||                OOOO  LL    ||
       1 ||                      LLLL  ||
       2 ||                            ||
       3 ||                        2222||
         ||||||||||||||||||||||||||||||||
    """

    blokus = init_blokus_duo()

    piece = Piece(blokus.shapes[ShapeKind.ONE])
    piece.set_anchor((0, 13))
    assert blokus.maybe_place(piece)

    piece = Piece(blokus.shapes[ShapeKind.C])
    piece.set_anchor((7, 3))
    assert blokus.maybe_place(piece)

    piece = Piece(blokus.shapes[ShapeKind.TWO])
    piece.set_anchor((13, 12))
    assert blokus.maybe_place(piece)

    piece = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece.set_anchor((8, 5))
    assert blokus.maybe_place(piece)

    piece = Piece(blokus.shapes[ShapeKind.THREE])
    piece.set_anchor((3, 11))
    assert blokus.maybe_place(piece)

    # Can't play 'O' again (not cool)
    piece = Piece(blokus.shapes[ShapeKind.LETTER_O])
    piece.set_anchor((9, 8))
    with pytest.raises(ValueError):
        blokus.maybe_place(piece)

    piece = Piece(blokus.shapes[ShapeKind.L])
    piece.set_anchor((10, 11))
    assert blokus.maybe_place(piece)

    piece = Piece(blokus.shapes[ShapeKind.FOUR])
    piece.set_anchor((4, 5))
    assert blokus.maybe_place(piece)

    assert blokus.curr_player == 2
    blokus.retire()
    assert blokus.curr_player == 1

    piece = Piece(blokus.shapes[ShapeKind.FIVE])
    piece.set_anchor((7, 0))
    assert blokus.maybe_place(piece)

    piece = Piece(blokus.shapes[ShapeKind.SEVEN])
    piece.set_anchor((4, 8))
    assert blokus.maybe_place(piece)

    assert blokus.get_score(1) == -(89 - 1 - 2 - 3 - 4 - 5 - 4)
    assert blokus.get_score(2) == -(89 - 3 - 4 - 5)

    assert blokus.grid[0][13] == (1, ShapeKind.ONE)
    assert blokus.grid[13][12] == (1, ShapeKind.TWO)
    assert blokus.grid[13][13] == (1, ShapeKind.TWO)
    assert blokus.grid[3][10] == (1, ShapeKind.THREE)
    assert blokus.grid[3][11] == (1, ShapeKind.THREE)
    assert blokus.grid[3][12] == (1, ShapeKind.THREE)
    assert blokus.grid[4][4] == (1, ShapeKind.FOUR)
    assert blokus.grid[4][5] == (1, ShapeKind.FOUR)
    assert blokus.grid[4][6] == (1, ShapeKind.FOUR)
    assert blokus.grid[4][7] == (1, ShapeKind.FOUR)
    assert blokus.grid[5][0] == (1, ShapeKind.FIVE)
    assert blokus.grid[6][0] == (1, ShapeKind.FIVE)
    assert blokus.grid[7][0] == (1, ShapeKind.FIVE)
    assert blokus.grid[8][0] == (1, ShapeKind.FIVE)
    assert blokus.grid[9][0] == (1, ShapeKind.FIVE)

    assert blokus.grid[7][3] == (2, ShapeKind.C)
    assert blokus.grid[7][4] == (2, ShapeKind.C)
    assert blokus.grid[8][3] == (2, ShapeKind.C)
    assert blokus.grid[8][5] == (2, ShapeKind.LETTER_O)
    assert blokus.grid[8][6] == (2, ShapeKind.LETTER_O)
    assert blokus.grid[9][5] == (2, ShapeKind.LETTER_O)
    assert blokus.grid[9][6] == (2, ShapeKind.LETTER_O)
    assert blokus.grid[9][8] is None, "Can't play 'O' again (not cool)"
    assert blokus.grid[9][9] is None, "Can't play 'O' again (not cool)"
    assert blokus.grid[10][8] is None, "Can't play 'O' again (not cool)"
    assert blokus.grid[10][9] is None, "Can't play 'O' again (not cool)"
    assert blokus.grid[8][11] == (2, ShapeKind.L)
    assert blokus.grid[9][11] == (2, ShapeKind.L)
    assert blokus.grid[10][11] == (2, ShapeKind.L)
    assert blokus.grid[11][11] == (2, ShapeKind.L)
    assert blokus.grid[11][12] == (2, ShapeKind.L)


def test_place_all_pieces_from_left_to_right_1() -> None:
    """
    Test that, after Player 1 retires,
    Player 2 can place all their pieces
      - at the very top of a board,
      - packed tightly from left to right, and
      - in the "canonical" order of shape kinds
        as defined in the ShapeKind enumeration.

                           1         2         3         4         5
    Column       012345678901234567890123456789012345678901234567890
                 |         |         |         |         |         |
    Origin Col   12  3  4  5 7 A C F S L N O  P|T  UV  W |X  Y Z   |
                 |         |         |         |         |         |
    Board Row 0  1223334444577 A CCFFSSL  NOOPPTTTU UV  W X  YZZ
                           5 7AAACFFSS L NNOOPP T UUUV WWXXXYY Z
                           5 7     F   L N   P  T  VVVWW  X  Y ZZ
                           5           LLN                   Y
                           5
    """

    # 48 columns is just wide enough
    blokus = BlokusFake(2, 48, {(0, 0), (1, 1)})

    def place_piece(kind: ShapeKind, row: int, col: int) -> None:
        """
        This helper function is called 21 times below,
        to place each one of Player 2's pieces at the
        designated positions
        """

        assert blokus.curr_player == 2
        assert not blokus.game_over

        piece = Piece(blokus.shapes[kind])

        # Before placing the piece at (row, col),
        # verify that one row higher is too high...
        piece.set_anchor((row - 1, col))
        assert not blokus.maybe_place(piece), (
            "Should have collied with wall (and maybe also previous piece):",
            f"Player {blokus.curr_player}, {str(kind)}, {row - 1}, {col}",
        )

        # ... and that one column left is too far left
        piece.set_anchor((row, col - 1))
        assert not blokus.maybe_place(piece), (
            "Should have collided with the previous piece:",
            f"Player {blokus.curr_player}, {str(kind)}, {row}, {col - 1}",
        )

        # Then place the piece tightly against the previous
        piece.set_anchor((row, col))
        assert blokus.maybe_place(piece), (
            "Should have just enough space to the right of previous piece:",
            f"Player {blokus.curr_player}, {str(kind)}, {row}, {col}",
        )

    assert blokus.curr_player == 1
    blokus.retire()

    assert blokus.curr_player == 2
    place_piece(ShapeKind.ONE, 0, 0)
    place_piece(ShapeKind.TWO, 0, 1)
    place_piece(ShapeKind.THREE, 0, 4)
    place_piece(ShapeKind.FOUR, 0, 7)
    place_piece(ShapeKind.FIVE, 2, 10)
    place_piece(ShapeKind.SEVEN, 1, 12)
    place_piece(ShapeKind.A, 1, 14)
    place_piece(ShapeKind.C, 0, 16)
    place_piece(ShapeKind.F, 1, 18)
    place_piece(ShapeKind.S, 0, 20)
    place_piece(ShapeKind.L, 2, 22)
    place_piece(ShapeKind.N, 1, 24)
    place_piece(ShapeKind.LETTER_O, 0, 26)
    place_piece(ShapeKind.P, 1, 29)
    place_piece(ShapeKind.T, 1, 31)
    place_piece(ShapeKind.U, 1, 34)
    place_piece(ShapeKind.V, 1, 35)
    place_piece(ShapeKind.W, 1, 38)
    place_piece(ShapeKind.X, 1, 41)
    place_piece(ShapeKind.Y, 1, 44)
    place_piece(ShapeKind.Z, 1, 46)

    assert blokus.game_over
    assert blokus.get_score(1) == -89
    assert blokus.get_score(2) == 0  # Bonus not implemented in BlokusFake
    assert blokus.winners == [2]


def test_place_all_pieces_from_left_to_right_2() -> None:
    """
    Test that Player 1 and Player 2 can place all
    their pieces packed tightly from left to right.
    Player 1 plays pieces in the "canonical" order
    of shape kinds, placing them at the very top of
    the board. Player 2 plays in reverse canonical
    order, placing pieces slighlty lower down on
    the board.

    In the following diagram, the top row of pieces
    is exactly the same as in the previous test case
    (test_place_all_pieces_from_left_to_right_1).
    This time, however, Player 1 is playing these
    pieces, and is alternating turns (with Player 2).

    Player 2's pieces are depicted slightly below
    using lowercase letters (and then digits) to
    indicate shape kinds.

                           1         2         3         4         5
    Column       012345678901234567890123456789012345678901234567890
                 |         |         |         |         |         |
    Origin Col   12  3  4  5 7 A C F S L N O  P|T  UV  W |X  Y Z   |
                 |         |         |         |         |         |
    Board Row 0  1223334444577 A CCFFSSL  NOOPPTTTU UV  W X  YZZ
              1  zz y x  w 5 7AAACFFSS L NNOOPP T UUUV WWXXXYY Z
              2   zyyxxxww 5 7 oo  F   L N   P  T  VVVWW  X  Y ZZ
              3   zzy xwwv 5tttoonl    LLN                    Y
              4     y    vu5utppnnl ss     5
              5        vvvuuutppn lssff    5
              6               p n llffcca7754444333221
              7                      fcaaa75
              8                           75
    """

    # 48 columns is just wide enough
    blokus = BlokusFake(2, 48, {(0, 0), (1, 1)})

    def place_piece_player(
        player: int, kind: ShapeKind, row: int, col: int
    ) -> None:
        assert blokus.curr_player == player
        assert not blokus.game_over

        piece = Piece(blokus.shapes[kind])

        # Before placing the piece at (row, col),
        # verify that one column left is too far left.
        # (Unlike the previous test case, not also
        # checking one row higher, because not all of
        # Player 2's pieces would have a collision.)

        piece.set_anchor((row, col - 1))
        assert not blokus.maybe_place(piece), (
            "Should have collided with the previous piece:",
            f"Player {blokus.curr_player}, {str(kind)}, {row}, {col - 1}",
        )

        # Then place the piece tightly against the previous
        piece.set_anchor((row, col))
        assert blokus.maybe_place(piece), (
            "Should have just enough space to the right of previous piece:",
            f"Player {blokus.curr_player}, {str(kind)}, {row}, {col}",
        )

    place_piece_player(1, ShapeKind.ONE, 0, 0)
    place_piece_player(2, ShapeKind.Z, 2, 1)

    place_piece_player(1, ShapeKind.TWO, 0, 1)
    place_piece_player(2, ShapeKind.Y, 2, 3)

    place_piece_player(1, ShapeKind.THREE, 0, 4)
    place_piece_player(2, ShapeKind.X, 2, 5)

    place_piece_player(1, ShapeKind.FOUR, 0, 7)
    place_piece_player(2, ShapeKind.W, 2, 7)

    place_piece_player(1, ShapeKind.FIVE, 2, 10)
    place_piece_player(2, ShapeKind.V, 4, 7)

    place_piece_player(1, ShapeKind.SEVEN, 1, 12)
    place_piece_player(2, ShapeKind.U, 5, 10)

    place_piece_player(1, ShapeKind.A, 1, 14)
    place_piece_player(2, ShapeKind.T, 4, 12)

    place_piece_player(1, ShapeKind.C, 0, 16)
    place_piece_player(2, ShapeKind.P, 5, 14)

    place_piece_player(1, ShapeKind.F, 1, 18)
    place_piece_player(2, ShapeKind.LETTER_O, 2, 14)

    place_piece_player(1, ShapeKind.S, 0, 20)
    place_piece_player(2, ShapeKind.N, 4, 15)

    place_piece_player(1, ShapeKind.L, 2, 22)
    place_piece_player(2, ShapeKind.L, 5, 17)

    place_piece_player(1, ShapeKind.N, 1, 24)
    place_piece_player(2, ShapeKind.S, 4, 19)

    place_piece_player(1, ShapeKind.LETTER_O, 0, 26)
    place_piece_player(2, ShapeKind.F, 6, 20)

    place_piece_player(1, ShapeKind.P, 1, 29)
    place_piece_player(2, ShapeKind.C, 6, 21)

    place_piece_player(1, ShapeKind.T, 1, 31)
    place_piece_player(2, ShapeKind.A, 7, 23)

    place_piece_player(1, ShapeKind.U, 1, 34)
    place_piece_player(2, ShapeKind.SEVEN, 7, 25)

    place_piece_player(1, ShapeKind.V, 1, 35)
    place_piece_player(2, ShapeKind.FIVE, 6, 26)

    place_piece_player(1, ShapeKind.W, 1, 38)
    place_piece_player(2, ShapeKind.FOUR, 6, 28)

    place_piece_player(1, ShapeKind.X, 1, 41)
    place_piece_player(2, ShapeKind.THREE, 6, 32)

    place_piece_player(1, ShapeKind.Y, 1, 44)
    place_piece_player(2, ShapeKind.TWO, 6, 34)

    place_piece_player(1, ShapeKind.Z, 1, 46)
    place_piece_player(2, ShapeKind.ONE, 6, 36)

    assert blokus.game_over
    assert blokus.get_score(1) == 0
    assert blokus.get_score(2) == 0  # Bonus not implemented in BlokusFake
    assert blokus.winners == [1, 2]


def simulate_moves(blokus: BlokusBase, pieces: list[Optional[Piece]]) -> None:
    """A simple interface for simulating a sequence of moves"""
    for piece in pieces:
        if piece is None:
            blokus.retire()
        else:
            blokus.maybe_place(piece)
