from datetime import date
import calendar as python_calendar

import flet as ft


# ---------------------------------------------------------
# Work schedule settings
# ---------------------------------------------------------

WORK_PATTERN = [
    "off",
    "on", "on", "on", "on", "on",
    "off", "off",
    "on", "on", "on", "on", "on", "on",
    "off", "off", "off",
]

REFERENCE_DATE = date(2026, 7, 16)
REFERENCE_CYCLE_POSITION = 6


def get_work_status(target_date: date) -> str:
    """Return 'on' or 'off' for any date."""

    days_difference = (target_date - REFERENCE_DATE).days

    cycle_position = (
        REFERENCE_CYCLE_POSITION + days_difference
    ) % len(WORK_PATTERN)

    return WORK_PATTERN[cycle_position]


# ---------------------------------------------------------
# Main Flet application
# ---------------------------------------------------------

def main(page: ft.Page):
    page.title = "Work Schedule"
    page.padding = 0
    page.spacing = 0

    # Let Flet adapt its controls to the current platform.
    page.adaptive = True

    today = date.today()

    displayed_year = today.year
    displayed_month = today.month
    selected_date = today

    # -----------------------------------------------------
    # Controls that will be updated later
    # -----------------------------------------------------

    month_title = ft.Text(
        size=22,
        weight=ft.FontWeight.BOLD,
    )

    selected_date_text = ft.Text(
        size=18,
        weight=ft.FontWeight.BOLD,
    )

    selected_status_text = ft.Text(
        size=26,
        weight=ft.FontWeight.BOLD,
    )

    selected_status_card = ft.Container(
        padding=20,
        border_radius=16,
        content=ft.Column(
            controls=[
                selected_date_text,
                selected_status_text,
            ],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    calendar_rows = ft.Column(
        spacing=6,
    )

    # -----------------------------------------------------
    # Update selected-date result
    # -----------------------------------------------------

    def update_selected_date(target_date: date):
        nonlocal selected_date

        selected_date = target_date
        status = get_work_status(target_date)

        selected_date_text.value = target_date.strftime(
            "%A, %d %B %Y"
        )

        if status == "on":
            selected_status_text.value = "ON DAY — WORKING"
            selected_status_text.color = ft.Colors.RED_700
            selected_status_card.bgcolor = ft.Colors.RED_50
            selected_status_card.border = ft.Border.all(
                2,
                ft.Colors.RED_200,
            )
        else:
            selected_status_text.value = "OFF DAY"
            selected_status_text.color = ft.Colors.GREEN_700
            selected_status_card.bgcolor = ft.Colors.GREEN_50
            selected_status_card.border = ft.Border.all(
                2,
                ft.Colors.GREEN_200,
            )

    # -----------------------------------------------------
    # Handle a date being tapped
    # -----------------------------------------------------

    def select_day(target_date: date):
        def handle_click(event):
            update_selected_date(target_date)
            build_calendar()
            page.update()

        return handle_click

    # -----------------------------------------------------
    # Create one calendar day box
    # -----------------------------------------------------

    def create_day_box(day_number: int | None):
        if day_number is None:
            # Empty space before or after the month's dates.
            return ft.Container(
                expand=True,
                height=56,
            )

        current_date = date(
            displayed_year,
            displayed_month,
            day_number,
        )

        status = get_work_status(current_date)

        if status == "on":
            background_colour = ft.Colors.RED_100
            text_colour = ft.Colors.RED_900
            status_label = "ON"
        else:
            background_colour = ft.Colors.GREEN_100
            text_colour = ft.Colors.GREEN_900
            status_label = "OFF"

        border = None

        if current_date == selected_date:
            border = ft.Border.all(
                3,
                ft.Colors.BLUE_700,
            )

        if current_date == today:
            border = ft.Border.all(
                3,
                ft.Colors.ORANGE_700,
            )

        # When today is also selected, use the blue selected border.
        if current_date == today and current_date == selected_date:
            border = ft.Border.all(
                3,
                ft.Colors.BLUE_700,
            )

        return ft.Container(
            expand=True,
            height=56,
            bgcolor=background_colour,
            border=border,
            border_radius=10,
            ink=True,
            on_click=select_day(current_date),
            content=ft.Column(
                controls=[
                    ft.Text(
                        str(day_number),
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=text_colour,
                    ),
                    ft.Text(
                        status_label,
                        size=9,
                        color=text_colour,
                    ),
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    # -----------------------------------------------------
    # Build the displayed month
    # -----------------------------------------------------

    def build_calendar():
        month_title.value = (
            f"{python_calendar.month_name[displayed_month]} "
            f"{displayed_year}"
        )

        calendar_rows.controls.clear()

        # monthcalendar returns a list of weeks.
        # Dates outside the displayed month are represented by 0.
        month_weeks = python_calendar.monthcalendar(
            displayed_year,
            displayed_month,
        )

        for week in month_weeks:
            week_controls = []

            for day_number in week:
                if day_number == 0:
                    week_controls.append(
                        create_day_box(None)
                    )
                else:
                    week_controls.append(
                        create_day_box(day_number)
                    )

            calendar_rows.controls.append(
                ft.Row(
                    controls=week_controls,
                    spacing=6,
                )
            )

    # -----------------------------------------------------
    # Previous and next month buttons
    # -----------------------------------------------------

    def previous_month(event):
        nonlocal displayed_month, displayed_year

        displayed_month -= 1

        if displayed_month == 0:
            displayed_month = 12
            displayed_year -= 1

        build_calendar()
        page.update()

    def next_month(event):
        nonlocal displayed_month, displayed_year

        displayed_month += 1

        if displayed_month == 13:
            displayed_month = 1
            displayed_year += 1

        build_calendar()
        page.update()

    def go_to_today(event):
        nonlocal displayed_month
        nonlocal displayed_year

        displayed_month = today.month
        displayed_year = today.year

        update_selected_date(today)
        build_calendar()
        page.update()

    # -----------------------------------------------------
    # Calendar headings
    # -----------------------------------------------------

    weekday_headings = ft.Row(
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    weekday,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_700,
                ),
            )
            for weekday in [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun",
            ]
        ],
        spacing=6,
    )

    legend = ft.Row(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        width=16,
                        height=16,
                        bgcolor=ft.Colors.RED_100,
                        border_radius=4,
                    ),
                    ft.Text("Working"),
                ],
                spacing=6,
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        width=16,
                        height=16,
                        bgcolor=ft.Colors.GREEN_100,
                        border_radius=4,
                    ),
                    ft.Text("Off"),
                ],
                spacing=6,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=24,
    )

    month_navigation = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.CHEVRON_LEFT,
                tooltip="Previous month",
                on_click=previous_month,
            ),
            month_title,
            ft.IconButton(
                icon=ft.Icons.CHEVRON_RIGHT,
                tooltip="Next month",
                on_click=next_month,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # -----------------------------------------------------
    # Initial display
    # -----------------------------------------------------

    update_selected_date(today)
    build_calendar()

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=ft.Padding.only(
                            left=20,
                            right=20,
                            top=18,
                            bottom=16,
                        ),
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Work Schedule",
                                    size=30,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "Tap a date to check whether it is "
                                    "an ON or OFF day.",
                                    color=ft.Colors.GREY_700,
                                ),
                            ],
                            spacing=4,
                        ),
                    ),

                    ft.Container(
                        expand=True,
                        padding=20,
                        content=ft.Column(
                            controls=[
                                selected_status_card,

                                month_navigation,

                                weekday_headings,

                                calendar_rows,

                                legend,

                                ft.Button(
                                    content="Go to today",
                                    icon=ft.Icons.TODAY,
                                    on_click=go_to_today,
                                ),
                            ],
                            spacing=14,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                    ),
                ],
                spacing=0,
            ),
        )
    )


ft.run(main, port = 8080)