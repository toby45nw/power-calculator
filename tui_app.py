"""
PowerCalc — Textual UI

Layout: a big answer readout, a command input, and three tabs
(History / Variables / Help). All calculator logic lives in
PowerCalc; this file only calls calc.execute(line) and displays
whatever Result comes back.
"""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    Input,
    Static,
    TabbedContent,
    TabPane,
)

from powerCalc import PowerCalc

# #answer is 6 rows tall with a 1-row border top and bottom, leaving 4 content
# rows. Keep this in sync if that CSS height changes.
ANSWER_CONTENT_ROWS = 4


def fmt(value):
    """15.0 -> '15', 2.5 -> '2.5', None -> a dash."""
    return "—" if value is None else f"{value:.10g}"


class AnswerPanel(Static):
    """The big readout below the input box.

    Builds every row of the box by hand (rather than leaving vertical
    centring to Textual) so the answer's position is exact, not a rounding
    guess. debug=True prefixes each row with its index, to check placement.
    """

    answer = reactive(None)
    status = reactive("")
    is_error = reactive(False)
    debug = reactive(True)

    def render(self) -> str:
        value_line = f"[bold #9ece6a]{fmt(self.answer)}[/]"
        if self.status:
            status_style = "red" if self.is_error else "dim"
            block = [value_line, f"[{status_style}]{self.status}[/]"]
        else:
            block = ["", value_line]  # leading blank nudges the number down a row

        top = (ANSWER_CONTENT_ROWS - len(block)) // 2
        lines = [""] * ANSWER_CONTENT_ROWS
        lines[top:top + len(block)] = block

        if self.debug:
            lines = [f"[dim]row {i}[/] {line}" for i, line in enumerate(lines)]

        return "\n".join(lines)


class HistoryTable(DataTable):
    """Command / result table. Selecting a row recalls that command."""

    def on_mount(self) -> None:
        self.add_columns("#", "Command", "Result")
        self.cursor_type = "row"
        self.zebra_stripes = True

    def rebuild(self, history):
        self.clear()
        for number, (line, result) in enumerate(history, 1):
            shown = result.error or result.message or fmt(result.value)
            style = "red" if result.error else ""
            self.add_row(str(number), line, f"[{style}]{shown}[/]" if style else shown)
        if history:
            self.move_cursor(row=len(history) - 1)


class VariablesTable(DataTable):
    def on_mount(self) -> None:
        self.add_columns("Name", "Value")

    def rebuild(self, variables):
        self.clear()
        for name, value in variables.items():
            self.add_row(name, fmt(value))


HELP_TEXT = """\
[bold]Commands[/bold]
  add / subtract / multiply / divide <n> [<n> ...] [-> var]
  set <n>                    5 x           (shorthand: store 5 in x)
  vars                       list variables
  clear                      clear the answer

[bold]Keys[/bold]
  Enter          run the command
  Up / Down      browse history (jumps to the History tab)
  Escape         back to a blank line
  Ctrl+Y         copy the answer
  Alt+1/2/3      switch tab
  Ctrl+Q         quit
"""


class PowerCalcApp(App):
    CSS = """
    Screen {
        background: #1a1b26;
    }
    #command-row {
        height: 3;
        margin: 1;
        border: round #7aa2f7;
    }
    #prompt {
        width: 3;
        content-align: center middle;
        color: #7aa2f7;
        text-style: bold;
    }
    #command {
        border: none;
        background: transparent;
        padding: 0 1 0 0;
    }
    #answer {
        height: 6;
        content-align: center middle;
        text-align: center;
        border: round #9ece6a;
        background: #1f2f28;
        margin: 0 1 1 1;
    }
    TabbedContent {
        margin: 0 1 1 1;
    }
    DataTable {
        height: auto;
        max-height: 16;
    }
    #help {
        padding: 1 2;
    }
    """

    # priority=True so these always work, even while the input box has focus.
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+y", "copy_answer", "Copy answer", priority=True),
        Binding("ctrl+d", "toggle_debug", "Toggle row numbers", priority=True),
        Binding("alt+1", "show_tab('history-tab')", "History", priority=True),
        Binding("alt+2", "show_tab('variables-tab')", "Variables", priority=True),
        Binding("alt+3", "show_tab('help-tab')", "Help", priority=True),
    ]

    def __init__(self):
        super().__init__()
        self.calc = PowerCalc()
        self.history_cursor = 0   # index into calc.history; len(history) = "not browsing"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="command-row"):
            yield Static(">", id="prompt")
            yield Input(id="command")
        yield AnswerPanel(id="answer")
        with TabbedContent(initial="history-tab"):
            with TabPane("History", id="history-tab"):
                yield HistoryTable(id="history")
            with TabPane("Variables", id="variables-tab"):
                yield VariablesTable(id="variables")
            with TabPane("Help", id="help-tab"):
                yield Static(HELP_TEXT, id="help")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#command", Input).focus()

    # -- running commands ------------------------------------------------

    def on_input_submitted(self, event: Input.Submitted) -> None:
        line = event.value
        result = self.calc.execute(line)
        event.input.value = ""
        self.history_cursor = len(self.calc.history)
        self.refresh_panels(result)

    def refresh_panels(self, result) -> None:
        answer = self.query_one("#answer", AnswerPanel)
        answer.answer = self.calc.state.get_ans()
        answer.is_error = bool(result.error)
        answer.status = result.error or result.message or ""

        self.query_one("#history", HistoryTable).rebuild(self.calc.history)
        self.query_one("#variables", VariablesTable).rebuild(self.calc.state.get_variables())

    # -- Up/Down: browse history straight from the input, no tabbing needed --

    def on_key(self, event) -> None:
        command = self.query_one("#command", Input)
        if not command.has_focus:
            return

        if event.key == "escape":
            # Jump straight back to a blank line, instead of pressing Down
            # all the way back from wherever you browsed to.
            self.history_cursor = len(self.calc.history)
            command.value = ""
            event.stop()
            return

        history = self.calc.history
        if not history or event.key not in ("up", "down"):
            return

        if event.key == "up":
            self.history_cursor = max(0, self.history_cursor - 1)
        else:
            self.history_cursor = min(len(history), self.history_cursor + 1)

        command.value = history[self.history_cursor][0] if self.history_cursor < len(history) else ""
        command.action_end()
        event.stop()

        # Jump to the History tab and highlight the matching row, so browsing
        # is visible without ever leaving the input box.
        self.query_one(TabbedContent).active = "history-tab"
        if self.history_cursor < len(history):
            self.query_one("#history", HistoryTable).move_cursor(row=self.history_cursor)

    # -- bindings ----------------------------------------------------------

    def action_copy_answer(self) -> None:
        answer = self.calc.state.get_ans()
        if answer is None:
            self.notify("Nothing to copy yet", severity="warning")
            return
        self.copy_to_clipboard(fmt(answer))
        self.notify(f"Copied {fmt(answer)}")

    def action_show_tab(self, tab_id: str) -> None:
        self.query_one(TabbedContent).active = tab_id

    def action_toggle_debug(self) -> None:
        answer = self.query_one("#answer", AnswerPanel)
        answer.debug = not answer.debug


if __name__ == "__main__":
    PowerCalcApp().run()