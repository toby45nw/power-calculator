from nicegui import ui

from powerCalc import PowerCalc

# ------------------------------------------------------------
# Calculator + the little bit of state the page needs
# ------------------------------------------------------------

calc = PowerCalc()
history = []                             # {"command", "text", "value"}, oldest first
status = {"text": "", "error": False}    # the line shown under the answer

COMMANDS = ["add", "subtract", "multiply", "divide", "set", "clear", "vars"]

# Tokyo Night palette
GREEN, RED, CYAN, MAGENTA, YELLOW, MUTED = "#9ece6a", "#f7768e", "#7dcfff", "#bb9af7", "#e0af68", "#565f89"
CARD = "w-full bg-[#24283b] rounded-xl p-4 gap-2"


def fmt(value):
    """15.0 -> '15', 2.5 -> '2.5', None -> a dash."""
    return "—" if value is None else f"{value:.10g}"


def handle(line):
    """Run one line through the calculator and record it. No UI code in here."""
    result = calc.execute(line)

    if result.error:
        status.update(text=result.error, error=True)
        return

    if result.message:
        text = result.message
    elif result.target == "ans":
        text = fmt(result.value)
    elif result.target:
        text = f"{result.target} = {fmt(result.value)}"
    else:
        return  # empty line

    status.update(text=text, error=False)
    history.append({"command": line.strip(), "text": text, "value": result.value})


# ------------------------------------------------------------
# Cards. Each one redraws itself when .refresh() is called.
# ------------------------------------------------------------

@ui.refreshable
def answer_card():
    answer = calc.state.get_ans()

    with ui.card().props("flat").classes(CARD + " items-center border border-[#9ece6a]/40 bg-[#1f2f28]"):
        ui.label("ANSWER").classes("text-xs tracking-widest").style(f"color: {GREEN}")
        ui.label(fmt(answer)).classes("text-8xl font-mono font-bold").style(f"color: {GREEN}")
        ui.label(status["text"] or " ").classes("font-mono").style(f"color: {RED if status['error'] else MUTED}")

        def copy():
            if answer is None:
                ui.notify("Nothing to copy yet", type="warning")
            else:
                ui.clipboard.write(fmt(answer))
                ui.notify(f"Copied {fmt(answer)}", type="positive")

        ui.button("Copy", icon="content_copy", on_click=copy).props("flat dense no-caps")


@ui.refreshable
def history_card(recall):
    with ui.card().props("flat").classes(CARD):
        ui.label("HISTORY").classes("text-xs tracking-widest").style(f"color: {CYAN}")
        if not history:
            ui.label("Nothing yet. Try: set 10").style(f"color: {MUTED}")
            return
        with ui.scroll_area().classes("w-full h-64"):
            for entry in reversed(history):
                row = ui.row().classes("w-full items-center no-wrap cursor-pointer rounded px-2 py-1 hover:bg-[#33467c]")
                row.on("click", lambda _, cmd=entry["command"]: recall(cmd))
                with row:
                    ui.label(entry["command"]).classes("font-mono grow")
                    ui.label(entry["text"]).classes("font-mono").style(f"color: {GREEN}")


@ui.refreshable
def variables_card():
    variables = calc.state.get_variables()

    with ui.card().props("flat").classes(CARD):
        ui.label("VARIABLES").classes("text-xs tracking-widest").style(f"color: {MAGENTA}")
        if not variables:
            ui.label("None yet. Try: 5 x").style(f"color: {MUTED}")
        for name, value in variables.items():
            with ui.row().classes("w-full justify-between font-mono"):
                ui.label(name).classes("font-bold").style(f"color: {MAGENTA}")
                ui.label(fmt(value)).style(f"color: {YELLOW}")


@ui.refreshable
def trend_card():
    values = [entry["value"] for entry in history if entry["value"] is not None]

    with ui.card().props("flat").classes(CARD):
        ui.label("RESULTS OVER TIME").classes("text-xs tracking-widest").style(f"color: {YELLOW}")
        if len(values) < 2:
            ui.label("Run a couple of commands to see the trend.").style(f"color: {MUTED}")
            return
        ui.echart({
            "backgroundColor": "transparent",
            "grid": {"left": 40, "right": 16, "top": 16, "bottom": 24},
            "xAxis": {"type": "category", "data": list(range(1, len(values) + 1)),
                      "axisLabel": {"color": MUTED}},
            "yAxis": {"type": "value", "axisLabel": {"color": MUTED},
                      "splitLine": {"lineStyle": {"color": "#2f3549"}}},
            "series": [{"type": "line", "data": values, "smooth": True,
                        "lineStyle": {"color": YELLOW, "width": 3},
                        "itemStyle": {"color": YELLOW},
                        "areaStyle": {"color": YELLOW, "opacity": 0.12}}],
        }).classes("w-full h-56")


def refresh_all():
    answer_card.refresh()
    history_card.refresh()
    variables_card.refresh()
    trend_card.refresh()


# ------------------------------------------------------------
# The page
# ------------------------------------------------------------

@ui.page("/")
def index():
    ui.query("body").style("background-color: #1a1b26")

    def submit():
        handle(entry.value)
        entry.value = ""
        refresh_all()

    def recall(command):
        entry.value = command
        entry.run_method("focus")

    def insert(word):
        entry.value = word + " "
        entry.run_method("focus")

    with ui.column().classes("w-full max-w-5xl mx-auto p-4 gap-4"):
        with ui.column().classes("w-full items-center gap-0"):
            ui.label("P O W E R C A L C").classes("text-3xl font-bold").style("color: #7aa2f7")
            ui.label("interactive calculator").style(f"color: {MUTED}")

        answer_card()

        entry = ui.input(placeholder="e.g.  add 5 3   ·   set 10   ·   5 x").props(
            'outlined autofocus input-class="font-mono text-lg"'
        ).classes("w-full")
        entry.on("keydown.enter", submit)

        with ui.row().classes("gap-1"):
            for word in COMMANDS:
                ui.button(word, on_click=lambda _, w=word: insert(w)).props("flat dense no-caps")

        with ui.grid(columns="3fr 2fr").classes("w-full gap-4"):
            history_card(recall)
            variables_card()

        trend_card()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="PowerCalc", dark=True, host="127.0.0.1", reload=False)