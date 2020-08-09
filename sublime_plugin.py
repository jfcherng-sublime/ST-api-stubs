# version: 4081

from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    ModuleType,
    Optional,
    Sequence,
    Set,
    Tuple,
    TypeVar,
    Union,
)
from typing_extensions import TypedDict

import importlib
import io
import sys
import threading
import time
import traceback

import sublime

# ----- #
# types #
# ----- #

_T = TypeVar("_T")

T_CALLBACK_0 = Callable[[], None]
T_CALLBACK_1 = Callable[[_T], None]
T_COMPLETION = Union[str, List[str], Tuple[str, str], sublime.CompletionItem]
T_COMPLETION_NORMALIZED = Tuple[
    # trigger
    str,
    # annotation
    str,
    # details
    str,
    # completion
    T_COMPLETION,
    # kind_name
    str,
    # letter
    str,
    # completion_format
    int,
    # flags
    int,
    # kind
    int,
]
T_EXPANDABLE_VAR = TypeVar("T_EXPANDABLE_VAR", str, List[str], Dict[str, str])
T_KIND = Tuple[int, str, str]
T_LAYOUT = TypedDict(
    "T_LAYOUT",
    # fmt: off
    {
        "cols": Sequence[float],
        "rows": Sequence[float],
        "cells": Sequence[Sequence[int]],
    },
    # fmt: on
)
T_LOCATION = Tuple[str, str, Tuple[int, int]]
T_POINT = int
T_STR = str  # alias in case we have a variable named as "str"
T_VALUE = Union[Dict, Set, List, Tuple, str, int, float, bool, None]
T_VECTOR = Tuple[float, float]


# -------- #
# ST codes #
# -------- #


api_ready: bool = False

deferred_plugin_loadeds = []

application_command_classes = []
window_command_classes = []
text_command_classes = []

view_event_listener_classes = []
view_event_listeners = {}

all_command_classes = [application_command_classes, window_command_classes, text_command_classes]

all_callbacks = {
    "on_init": [],
    "on_new": [],
    "on_clone": [],
    "on_load": [],
    "on_revert": [],
    "on_reload": [],
    "on_pre_close": [],
    "on_close": [],
    "on_pre_save": [],
    "on_post_save": [],
    "on_pre_move": [],
    "on_post_move": [],
    "on_modified": [],
    "on_selection_modified": [],
    "on_activated": [],
    "on_deactivated": [],
    "on_query_context": [],
    "on_query_completions": [],
    "on_hover": [],
    "on_text_command": [],
    "on_window_command": [],
    "on_post_text_command": [],
    "on_post_window_command": [],
    "on_modified_async": [],
    "on_selection_modified_async": [],
    "on_pre_save_async": [],
    "on_post_save_async": [],
    "on_post_move_async": [],
    "on_activated_async": [],
    "on_deactivated_async": [],
    "on_new_async": [],
    "on_load_async": [],
    "on_revert_async": [],
    "on_reload_async": [],
    "on_clone_async": [],
    "on_new_buffer": [],
    "on_new_buffer_async": [],
    "on_close_buffer": [],
    "on_close_buffer_async": [],
    "on_new_project": [],
    "on_new_project_async": [],
    "on_load_project": [],
    "on_load_project_async": [],
    "on_pre_save_project": [],
    "on_post_save_project": [],
    "on_post_save_project_async": [],
    "on_pre_close_project": [],
    "on_new_window": [],
    "on_new_window_async": [],
    "on_pre_close_window": [],
    "on_exit": [],
}

pending_on_activated_async_lock = threading.Lock()

pending_on_activated_async_callbacks = {"EventListener": [], "ViewEventListener": []}

view_event_listener_excluded_callbacks: Set[str] = {
    "on_clone",
    "on_clone_async",
    "on_exit",
    "on_init",
    "on_load_project",
    "on_load_project_async",
    "on_new",
    "on_new_async",
    "on_new_buffer",
    "on_new_buffer_async",
    "on_close_buffer",
    "on_close_buffer_async",
    "on_new_project",
    "on_new_project_async",
    "on_new_window",
    "on_new_window_async",
    "on_post_save_project",
    "on_post_save_project_async",
    "on_post_window_command",
    "on_pre_close_project",
    "on_pre_close_window",
    "on_pre_save_project",
    "on_window_command",
}

text_change_listener_classes = []
text_change_listener_callbacks: Set[str] = {
    "on_text_changed",
    "on_text_changed_async",
    "on_revert",
    "on_revert_async",
    "on_reload",
    "on_reload_async",
}

profile: Dict[str, Dict[str, Any]] = {}


def add_profiling(event_handler: Callable) -> Callable:
    """
    Decorator to measure blocking event handler methods. Also prevents
    exceptions from interrupting other events handlers.

    :param event_handler:
        The event handler method - must be an unbound method

    :return:
        The decorated method
    """
    ...


def trap_exceptions(event_handler: Callable) -> Callable:
    """
    Decorator to prevent exceptions from interrupting other events handlers.

    :param event_handler:
        The event handler method - must be an unbound method

    :return:
        The decorated method
    """
    ...


def decorate_handler(cls: _T, method_name: str) -> None:
    """
    Decorates an event handler method with exception trapping, and in the case
    of blocking calls, profiling.

    :param cls:
        The class object to decorate

    :param method_name:
        A unicode string of the name of the method to decorate
    """
    ...


def unload_module(module: ModuleType) -> None:
    ...


def unload_plugin(modulename: str) -> None:
    ...


def reload_plugin(modulename: str) -> None:
    ...


def load_module(m: ModuleType) -> None:
    ...


def synthesize_on_activated_async() -> None:
    ...


def _instantiation_error(cls: _T, e: Exception) -> None:
    ...


def notify_application_commands() -> None:
    ...


def create_application_commands():
    cmds = []
    for cls in application_command_classes:
        try:
            o = cls()
            cmds.append((o, o.name()))
        except Exception as e:
            _instantiation_error(cls, e)
    return cmds


def create_window_commands(window_id: int):
    window = sublime.Window(window_id)
    cmds = []
    for cls in window_command_classes:
        try:
            o = cls(window)
            cmds.append((o, o.name()))
        except Exception as e:
            _instantiation_error(cls, e)
    return cmds


def create_text_commands(view_id: int):
    view = sublime.View(view_id)
    cmds = []
    for cls in text_command_classes:
        try:
            o = cls(view)
            cmds.append((o, o.name()))
        except Exception as e:
            _instantiation_error(cls, e)
    return cmds


def on_api_ready() -> None:
    ...


def is_view_event_listener_applicable(cls, view: sublime.View) -> bool:
    ...


def create_view_event_listeners(classes, view: sublime.View) -> None:
    ...


def check_view_event_listeners(view: sublime.View) -> None:
    ...


def attach_view(view: sublime.View) -> None:
    ...


check_all_view_event_listeners_scheduled: bool = False


def check_all_view_event_listeners() -> None:
    ...


def detach_view(view: sublime.View) -> None:
    ...


def find_view_event_listener(view: sublime.View, cls):
    if view.view_id in view_event_listeners:
        for vel in view_event_listeners[view.view_id]:
            if vel.__class__ == cls:
                return vel
    return None


def attach_buffer(buf: sublime.Buffer) -> None:
    ...


def plugin_module_for_obj(obj: _T) -> str:
    ...


def el_callbacks(name, listener_only=False):
    for el in all_callbacks[name]:
        yield el if listener_only else getattr(el, name)


def vel_callbacks(v, name, listener_only=False):
    for vel in view_event_listeners.get(v.view_id, []):
        if not hasattr(vel, name):
            continue
        yield vel if listener_only else getattr(vel, name)


def run_view_callbacks(name: str, view_id: int, *args: T_VALUE, attach: bool = False, el_only: bool = False,) -> None:
    ...


def run_window_callbacks(name: str, window_id: int, *args: T_VALUE) -> None:
    ...


def on_init(module: str) -> None:
    """
    Trigger the on_init() methods on EventListener and ViewEventListener
    objects. This is method that allows event listeners to run something
    once per view, even if the view is done loading before the listener
    starts listening.

    :param module:
        A unicode string of the name of a plugin module to filter listeners by
    """
    ...


def on_new(view_id: int) -> None:
    ...


def on_new_async(view_id: int) -> None:
    ...


def on_new_buffer(buffer_id: int) -> None:
    ...


def on_new_buffer_async(buffer_id: int) -> None:
    ...


def on_close_buffer(buffer_id: int) -> None:
    ...


def on_close_buffer_async(buffer_id: int) -> None:
    ...


def on_clone(view_id: int) -> None:
    ...


def on_clone_async(view_id: int) -> None:
    ...


class Summary:
    max: float
    sum: float
    count: int

    def __init__(self) -> None:
        ...

    def record(self, x: float) -> None:
        ...


def get_profiling_data() -> List[Tuple[str, str, int, float, float]]:
    ...


def on_load(view_id: int) -> None:
    ...


def on_load_async(view_id: int) -> None:
    ...


def on_revert(view_id: int) -> None:
    ...


def on_revert_async(view_id: int) -> None:
    ...


def on_reload(view_id: int) -> None:
    ...


def on_reload_async(view_id: int) -> None:
    ...


def on_pre_close(view_id: int) -> None:
    ...


def on_close(view_id) -> None:
    ...


def on_pre_save(view_id: int) -> None:
    ...


def on_pre_save_async(view_id: int) -> None:
    ...


def on_post_save(view_id: int) -> None:
    ...


def on_post_save_async(view_id: int) -> None:
    ...


def on_pre_move(view_id: int) -> None:
    ...


def on_post_move(view_id: int) -> None:
    ...


def on_post_move_async(view_id: int) -> None:
    ...


def on_modified(view_id: int) -> None:
    ...


def on_modified_async(view_id: int) -> None:
    ...


def on_selection_modified(view_id: int) -> None:
    ...


def on_selection_modified_async(view_id: int) -> None:
    ...


def on_activated(view_id: int) -> None:
    ...


def on_activated_async(view_id: int) -> None:
    ...


def on_deactivated(view_id: int) -> None:
    ...


def on_deactivated_async(view_id: int) -> None:
    ...


def on_query_context(view_id: int, key: str, operator: str, operand: T_VALUE, match_all: bool) -> bool:
    ...


def normalise_completion(
    c: Union[sublime.CompletionItem, str, Sequence[str], Sequence[str, str], Sequence[str, str, str]]
) -> T_COMPLETION_NORMALIZED:
    ...


class MultiCompletionList:
    remaining_calls: int
    view_id: int
    req_id: int
    completions: List[T_COMPLETION_NORMALIZED]
    flags: int

    def __init__(self, num_completion_lists: int, view_id: int, req_id: int) -> None:
        ...

    def completions_ready(
        self,
        completions: Iterable[
            Union[sublime.CompletionItem, str, Sequence[str], Sequence[str, str], Sequence[str, str, str],]
        ],
        flags: int,
    ) -> None:
        ...


def on_query_completions(view_id: int, req_id: int, prefix: str, locations: List[T_POINT]) -> None:
    ...


def on_hover(view_id: int, point: T_POINT, hover_zone: int) -> None:
    ...


def on_text_command(view_id: int, name: str, args: Optional[Dict[str, T_VALUE]]) -> Tuple[str, Optional[Dict]]:
    ...


def on_window_command(window_id: int, name: str, args: Optional[Dict[str, T_VALUE]]) -> Tuple[str, Optional[Dict]]:
    ...


def on_post_text_command(view_id: int, name: str, args: Optional[Dict[str, T_VALUE]]) -> None:
    ...


def on_post_window_command(window_id: int, name: str, args: Optional[Dict[str, T_VALUE]]) -> None:
    ...


def on_new_project(window_id: int) -> None:
    ...


def on_new_project_async(window_id: int) -> None:
    ...


def on_load_project(window_id: int) -> None:
    ...


def on_load_project_async(window_id: int) -> None:
    ...


def on_pre_save_project(window_id: int) -> None:
    ...


def on_post_save_project(window_id: int) -> None:
    ...


def on_post_save_project_async(window_id: int) -> None:
    ...


def on_pre_close_project(window_id: int) -> None:
    ...


def on_new_window(window_id: int) -> None:
    ...


def on_new_window_async(window_id: int) -> None:
    ...


def on_pre_close_window(window_id: int) -> None:
    ...


def on_exit(log_path: str) -> None:
    ...


class CommandInputHandler:
    def name(self) -> str:
        """
        The command argument name this input handler is editing.
        Defaults to `foo_bar` for an input handler named `FooBarInputHandler`.
        """
        ...

    def next_input(self, args: Dict[str, T_VALUE]) -> Optional["CommandInputHandler"]:
        """
        Returns the next input after the user has completed this one.
        May return None to indicate no more input is required,
        or `sublime_plugin.BackInputHandler()` to indicate that
        the input handler should be poped off the stack instead.
        """
        ...

    def placeholder(self) -> str:
        """
        Placeholder text is shown in the text entry box before the user has entered anything.
        Empty by default.
        """
        ...

    def initial_text(self) -> str:
        """ Initial text shown in the text entry box. Empty by default. """
        ...

    def initial_selection(self) -> List:
        """
        @todo List of what???
        """
        ...

    def preview(self, arg: Dict[str, T_VALUE]) -> Union[str, sublime.Html]:
        """
        Called whenever the user changes the text in the entry box.
        The returned value (either plain text or HTML) will be shown in the preview area of the Command Palette.
        """
        ...

    def validate(self, arg: Dict[str, T_VALUE]) -> bool:
        """
        Called whenever the user presses enter in the text entry box.
        Return False to disallow the current value.
        """
        ...

    def cancel(self) -> None:
        """ Called when the input handler is canceled, either by the user pressing backspace or escape. """
        ...

    def confirm(self, text: Dict[str, T_VALUE]) -> None:
        """ Called when the input is accepted, after the user has pressed enter and the text has been validated. """
        ...

    def create_input_handler_(self, args: Dict[str, T_VALUE]) -> Optional["CommandInputHandler"]:
        ...

    def preview_(self, v: str) -> Tuple[str, int]:
        ...

    def validate_(self, v: str) -> bool:
        ...

    def cancel_(self) -> None:
        ...

    def confirm_(self, v: str) -> None:
        ...


class BackInputHandler(CommandInputHandler):
    def name(self) -> str:
        """ The command argument name this input handler is editing. Defaults to `_Back`. """
        ...


class TextInputHandler(CommandInputHandler):
    """
    TextInputHandlers can be used to accept textual input in the Command Palette.
    Return a subclass of this from the `input()` method of a command.
    """

    def description(self, text: str) -> str:
        """
        The text to show in the Command Palette when this input handler is not at the top of the input handler stack.
        Defaults to the text the user entered.
        """
        ...

    def setup_(self, args: Dict[str, T_VALUE]) -> Tuple[list, Dict[str, str]]:
        ...

    def description_(self, v: str, text: str) -> str:
        ...


class ListInputHandler(CommandInputHandler):
    """
    ListInputHandlers can be used to accept a choice input from a list items in the Command Palette.
    Return a subclass of this from the input() method of a command.
    """

    def list_items(
        self,
    ) -> Union[
        List[str], List[Tuple[str, T_VALUE]], Tuple[Union[List[str], List[Tuple[str, T_VALUE]]], int],
    ]:
        """
        The items to show in the list. If returning a list of `(str, value)` tuples,
        then the str will be shown to the user, while the value will be used as the command argument.

        Optionally return a tuple of `(list_items, selected_item_index)` to indicate an initial selection.
        """
        ...

    def description(self, v: str, text: str) -> str:
        """
        The text to show in the Command Palette when this input handler is not at the top of the input handler stack.
        Defaults to the text of the list item the user selected.
        """
        ...

    def setup_(self, args: Dict[str, T_VALUE]) -> Tuple[List[Tuple[str, T_VALUE]], Dict[str, str]]:
        ...

    def description_(self, v: str, text: str) -> str:
        ...


class Command:
    def name(self) -> str:
        """
        The command argument name this input handler is editing.
        Defaults to `foo_bar` for an input handler named `FooBarInputHandler`.
        """
        ...

    def is_enabled_(self, args: Dict[str, T_VALUE]) -> bool:
        ...

    def is_enabled(self) -> bool:
        """
        Returns True if the command is able to be run at this time.
        The default implementation simply always returns True.
        """
        ...

    def is_visible_(self, args: Dict[str, T_VALUE]) -> bool:
        ...

    def is_visible(self) -> bool:
        """
        Returns True if the command should be shown in the menu at this time.
        The default implementation always returns True.
        """
        ...

    def is_checked_(self, args: Dict[str, T_VALUE]) -> bool:
        ...

    def is_checked(self) -> bool:
        """
        Returns True if a checkbox should be shown next to the menu item.
        The `.sublime-menu` file must have the "checkbox key set to true for this to be used.
        """
        ...

    def description_(self, args: Dict[str, T_VALUE]) -> str:
        ...

    def description(self) -> str:
        """
        Returns a description of the command with the given arguments.
        Used in the menus, and for Undo / Redo descriptions.
        Return None to get the default description.
        """
        ...

    def filter_args(self, args: Dict[str, T_VALUE]) -> Dict[str, T_VALUE]:
        """ Returns the args after without the "event" entry """
        ...

    def want_event(self) -> bool:
        """
        Return True to receive an event argument when the command is triggered by a mouse action.
        The event information allows commands to determine which portion of the view was clicked on.
        The default implementation returns False.
        """
        ...

    def input(self, args: Dict[str, T_VALUE]) -> Optional[CommandInputHandler]:
        """
        If this returns something other than None,
        the user will be prompted for an input before the command is run in the Command Palette.
        """
        ...

    def input_description(self) -> str:
        """
        Allows a custom name to be show to the left of the cursor in the input box,
        instead of the default one generated from the command name.
        """
        ...

    def create_input_handler_(self, args: Dict[str, T_VALUE]) -> Optional[CommandInputHandler]:
        ...


class ApplicationCommand(Command):
    """ ApplicationCommands are instantiated once per application. """

    def run_(self, edit_token: int, args: Dict[str, T_VALUE]) -> None:
        ...

    def run(self) -> None:
        """ Called when the command is run """
        ...


class WindowCommand(Command):
    """ WindowCommands are instantiated once per window. The Window object may be retrieved via `self.window` """

    window: sublime.Window

    def __init__(self, window: sublime.Window) -> None:
        ...

    def run_(self, edit_token: int, args: Dict[str, T_VALUE]) -> None:
        ...

    def run(self) -> None:
        """ Called when the command is run """
        ...


class TextCommand(Command):
    """ TextCommands are instantiated once per view. The View object may be retrieved via `self.view` """

    view: sublime.View

    def __init__(self, view: sublime.View) -> None:
        ...

    def run_(self, edit_token: int, args: Dict[str, T_VALUE]) -> None:
        ...

    def run(self, edit: sublime.Edit):
        """ Called when the command is run """
        ...


class EventListener:
    pass


class ViewEventListener:
    """
    A class that provides similar event handling to EventListener, but bound to a specific view.
    Provides class method-based filtering to control what views objects are created for.

    The view is passed as a single parameter to the constructor.
    The default implementation makes the view available via `self.view`.
    """

    view: sublime.View

    @classmethod
    def is_applicable(cls, settings: sublime.Settings) -> bool:
        """
        Receives a Settings object and should return a bool
        indicating if this class applies to a view with those settings.
        """
        ...

    @classmethod
    def applies_to_primary_view_only(cls) -> bool:
        """
        Returns a bool indicating if this class applies only to the primary view for a file.
        A view is considered primary if it is the only, or first, view into a file.
        """
        ...

    def __init__(self, view: sublime.View) -> None:
        ...


class TextChangeListener:
    """ Base implementation of a text change listener.

    An instance may be added to a view using `sublime.View.add_text_listener`.

    Has the following callbacks:

    on_text_changed(changes):
        Called when text is changed in a buffer.

        :param changes:
            A list of TextChange

    on_text_changed_async(changes):
        Async version of on_text_changed_async.

    on_revert():
        Called when the buffer is reverted.

        A revert does not trigger text changes. If the contents of the buffer
        are required here use View.substr()

    on_revert_async():
        Async version of on_revert_async.

    on_reload():
        Called when the buffer is reloaded.

        A reload does not trigger text changes. If the contents of the buffer
        are required here use View.substr()

    on_reload_async():
        Async version of on_reload_async.
    """

    __key: Optional[int] = None
    buffer: Optional[sublime.Buffer] = None

    @classmethod
    def is_applicable(cls, buffer: sublime.Buffer) -> bool:
        """
        Receives a Buffer object and should return a bool
        indicating if this class applies to a view with the Buffer.
        """
        ...

    def __init__(self, buffer: sublime.Buffer) -> None:
        ...

    def remove(self) -> None:
        """
        Remove this listener from the buffer.

        Async callbacks may still be called after this, as they are queued separately.
        """
        ...

    def attach(self, buffer: sublime.Buffer) -> None:
        """ Attach this listener to a buffer. """
        ...

    def is_attached(self) -> bool:
        """
        Check whether the listener is receiving events from a buffer.
        May not be called from __init__.
        """
        ...


class MultizipImporter(importlib.abc.MetaPathFinder):
    def __init__(self):
        self.loaders = []

    def _make_spec(self, loader: importlib.abc.Loader, fullname: str) -> importlib.machinery.ModuleSpec:
        """
        :param loader:
            The importlib.abc.Loader to create the ModuleSpec from

        :param fullname:
            A unicode string of the module name

        :return:
            An instance of importlib.machinery.ModuleSpec()
        """
        ...

    def find_spec(
        self, fullname: str, path: Optional[List[str]], target: Optional[Any] = None
    ) -> Optional[importlib.machinery.ModuleSpec]:
        """
        :param fullname:
            A unicode string of the module name

        :param path:
            None or a list with a single unicode string of the __path__ of
            the parent module if importing a submodule

        :param target:
            Unused - extra info that importlib may provide?

        :return:
            An importlib.machinery.ModuleSpec() object
        """
        ...


class ZipResourceReader(importlib.abc.ResourceReader):
    """
    Implements the resource reader interface introduced in Python 3.7
    """

    loader: "ZipLoader"
    fullname: str

    def __init__(self, loader: "ZipLoader", fullname: str) -> None:
        """
        :param loader:
            The source ZipLoader() object

        :param fullname:
            A unicode string of the module name to load resources for
        """
        ...

    def open_resource(self, resource: str) -> io.BytesIO:
        """
        :param resource:
            A unicode string of a resource name - should not contain a path
            separator

        :raises:
            FileNotFoundError - when the resource doesn't exist

        :return:
            An io.BytesIO() object
        """
        ...

    def resource_path(self, resource: str) -> None:
        """
        :param resource:
            A unicode string of a resource name - should not contain a path
            separator

        :raises:
            FileNotFoundError - always, since there is no normal filesystem access
        """
        ...

    def is_resource(self, name: str) -> bool:
        """
        :param name:
            A unicode string of a file name to check if it is a resource

        :return:
            A boolean indicating if the file is a resource
        """
        ...

    def contents(self) -> List[str]:
        """
        :return:
            A list of the resources for this module
        """
        ...


class ZipLoader(importlib.abc.InspectLoader):
    """
    A custom Python loader that handles loading .py and .pyc files from
    .sublime-package zip files, and supports overrides where a loose file in
    the Packages/ folder of the data dir may be loaded instead of a file in
    the .sublime-package file.
    """

    zippath: str
    name: str

    contents: Dict[str, str]
    filenames: Dict[str, str]
    packages: Set[str]
    resources: Dict[str, Dict[str, str]]
    refreshed: float

    def __init__(self, zippath: str) -> None:
        """
        :param zippath:
            A unicode string of the full filesystem path to the zip file
        """
        ...

    def _get_name_key(self, fullname: str) -> Union[Tuple[None, None], Tuple[str, str]]:
        """
        Converts a module name into a pair of package name and key. The
        key is used to access the various data structures in this object.

        :param fullname:
            A unicode string of a module name

        :return:
            If the fullname is not a module in this package, (None, None),
            otherwise a 2-element tuple of unicode strings. The first element
            being the package name, and the second being a sub-module, e.g.
            ("Default", "indentation").
        """
        ...

    def has(self, fullname: str) -> bool:
        """
        Checks if the module is handled by this loader

        :param fullname:
            A unicode string of the module to check

        :return:
            A boolean if the module is handled by this loader
        """
        ...

    def get_resource_reader(self, fullname: str) -> Optional[importlib.abc.ResourceReader]:
        """
        :param fullname:
            A unicode string of the module name to get the resource reader for

        :return:
            None if the module is not a package, otherwise an object that
            implements the importlib.abc.ResourceReader() interface
        """
        ...

    def get_filename(self, fullname: str) -> str:
        """
        :param fullname:
            A unicode string of the module name

        :raises:
            ImportError - when the module has no file path

        :return:
            A unicode string of the file path to the module
        """
        ...

    def get_code(self, fullname: str) -> Any:
        """
        :param fullname:
            A unicode string of the module to get the code for

        :raises:
            ModuleNotFoundError - when the module is not part of this zip file
            ImportError - when there is an error loading the code

        :return:
            A code object for the module
        """
        ...

    def get_source(self, fullname: str) -> Optional[str]:
        """
        :param fullname:
            A unicode string of the module to get the source for

        :raises:
            ModuleNotFoundError - when the module is not part of this zip file
            ImportError - when there is an error loading the source file

        :return:
            A unicode string of the source code, or None if there is no source
            for the module (i.e. a .pyc file)
        """
        ...

    def _load_source(self, fullname: str, path) -> str:
        """
        Loads the source code to the module

        :param fullname:
            A unicode string of the module name

        :param path:
            A filesystem path to the module - may be a path into s
            .sublime-package file

        :return:
            A unicode string
        """
        ...

    def is_package(self, fullname: str) -> bool:
        """
        :param fullname:
            A unicode string of the module to see if it is a package

        :return:
            A boolean if the module is a package
        """
        ...

    def _spec_info(self, fullname: str) -> Union[Tuple[None, None], Tuple[str, bool]]:
        """
        :param fullname:
            A unicode string of the module that an
            importlib.machinery.ModuleSpec() object is going to be created for

        :return:
            A 2-element tuple of:
             - (None, None) if the loader does not know about the module
             - (unicode string, bool) of the origin and is_package params to
               pass to importlib.machinery.ModuleSpec()
        """
        ...

    def _scan_zip(self):
        """
        Rebuild the internal cached info about the contents of the zip
        """
        ...


override_path: Optional[str] = None
multi_importer: MultizipImporter = MultizipImporter()
sys.meta_path.insert(0, multi_importer)


def update_compressed_packages(pkgs: Iterable[str]) -> None:
    ...


def set_override_path(path: str) -> None:
    ...
