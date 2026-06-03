import flet as ft


def calculate_winner(squares: list[str]):
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6],
    ]
    for a, b, c in lines:
        if squares[a] and squares[a] == squares[b] == squares[c]:
            return squares[a], [a, b, c]
    return None


def make_square(index: int) -> tuple[ft.Container, ft.Container]:
    """Returns (outer_container, icon_container)"""
    icon_container = ft.Container(
        content=ft.Icon(ft.Icons.STAR, size=30, color=ft.Colors.AMBER),
        scale=0,
        animate_scale=ft.Animation(300, ft.AnimationCurve.BOUNCE_OUT),
    )
    outer = ft.Container(
        content=icon_container,
        width=60,
        height=60,
        border=ft.Border.all(2, ft.Colors.OUTLINE),
        border_radius=8,
        alignment=ft.Alignment.CENTER,
        animate=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
        data=index,
    )
    return outer, icon_container


def main(page: ft.Page):
    page.title = "Tic-Tac-Toe"

    squares: list[str] = [""] * 9
    history: list[list[str]] = [squares[:]]
    current_move_ref = [0]

    # Build 9 squares
    outers = []
    icons = []
    for i in range(9):
        o, ic = make_square(i)
        outers.append(o)
        icons.append(ic)

    # Status / winner message
    status_text = ft.Text("Next: ⭐", size=20, weight=ft.FontWeight.BOLD)
    winner_container = ft.Container(
        content=ft.Text("", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        bgcolor=ft.Colors.PURPLE_400,
        border_radius=12,
        padding=ft.Padding.symmetric(horizontal=20, vertical=10),
        scale=0,
        animate_scale=ft.Animation(500, ft.AnimationCurve.BOUNCE_OUT),
        visible=False,
    )

    def refresh_board():
        sq = history[current_move_ref[0]]
        result = calculate_winner(sq)
        winning = result[1] if result else []

        for i, (outer, ic) in enumerate(zip(outers, icons)):
            val = sq[i]
            # icon
            if val == "X":
                ic.content = ft.Icon(ft.Icons.STAR, size=30, color=ft.Colors.AMBER)
            elif val == "O":
                ic.content = ft.Icon(ft.Icons.FAVORITE, size=30, color=ft.Colors.PINK)
            ic.scale = 1 if val else 0
            # highlight
            outer.bgcolor = ft.Colors.YELLOW_200 if i in winning else None
            # click handler
            outer.on_click = handle_click if not result and not val else None
        page.update()

        if result:
            winner, _ = result
            label = "⭐ WIN!" if winner == "X" else "💜 WIN!"
            winner_container.content.value = label
            winner_container.visible = True
            winner_container.scale = 1
            winner_container.update()

    def handle_click(e: ft.ControlEvent):
        i: int = e.control.data
        sq = history[current_move_ref[0]]
        if sq[i] or calculate_winner(sq):
            return
        next_sq = sq[:]
        x_is_next = current_move_ref[0] % 2 == 0
        next_sq[i] = "X" if x_is_next else "O"
        next_history = history[: current_move_ref[0] + 1] + [next_sq]
        history.clear()
        history.extend(next_history)
        current_move_ref[0] = len(next_history) - 1

        # pop-in animation for clicked square only
        ic = icons[i]
        if next_sq[i] == "X":
            ic.content = ft.Icon(ft.Icons.STAR, size=30, color=ft.Colors.AMBER)
        else:
            ic.content = ft.Icon(ft.Icons.FAVORITE, size=30, color=ft.Colors.PINK)
        ic.scale = 1
        ic.update()

        result = calculate_winner(next_sq)
        winning = result[1] if result else []
        for idx, outer in enumerate(outers):
            outer.bgcolor = ft.Colors.YELLOW_200 if idx in winning else None
            outer.on_click = handle_click if not result and not next_sq[idx] else None
        page.update()

        if result:
            winner, _ = result
            label = "⭐ WIN!" if winner == "X" else "💜 WIN!"
            winner_container.content.value = label
            winner_container.visible = True
            winner_container.scale = 1
            winner_container.update()
            status_text.value = ""
        else:
            next_player = "💜" if x_is_next else "⭐"
            status_text.value = f"Next: {next_player}"
        status_text.update()
        history_col.controls = build_history_buttons()
        history_col.update()

    def jump_to(move: int):
        current_move_ref[0] = move
        winner_container.scale = 0
        winner_container.visible = False
        winner_container.update()
        x_is_next = move % 2 == 0
        status_text.value = f"Next: {'⭐' if x_is_next else '💜'}"
        refresh_board()
        history_col.controls = build_history_buttons()
        history_col.update()

    def build_history_buttons():
        return [
            ft.TextButton(
                f"Go to move #{m}" if m > 0 else "Go to game start",
                on_click=lambda e, m=m: jump_to(m),
            )
            for m in range(len(history))
        ]

    history_col = ft.Column(build_history_buttons())

    board = ft.Column(
        [ft.Row([outers[i] for i in row]) for row in [(0,1,2),(3,4,5),(6,7,8)]],
        spacing=4,
    )

    # Attach click handlers initially
    for outer in outers:
        outer.on_click = handle_click

    page.add(
        ft.SafeArea(
            content=ft.Row(
                [
                    ft.Column([status_text, winner_container, board]),
                    history_col,
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
