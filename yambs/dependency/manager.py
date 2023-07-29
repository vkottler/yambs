"""
A module implementing a dependency manager.
"""

# built-in
from pathlib import Path
from typing import List, Set

# third-party
from vcorelib.io import ARBITER
from vcorelib.logging import LoggerType
from vcorelib.paths import set_exec_flags

# internal
from yambs.dependency.config import Dependency, DependencyData
from yambs.dependency.handlers import HANDLERS
from yambs.dependency.handlers.types import DependencyTask
from yambs.dependency.state import DependencyState


class DependencyManager:
    """A class for managing project dependencies."""

    def __init__(self, root: Path) -> None:
        """Initialize this instance."""

        self.root = root
        self.state_path = self.root.joinpath("state.json")
        self.state = ARBITER.decode(self.state_path).data

        # A place for third-party include roots to be linked.
        self.include = self.root.joinpath("include")
        self.include.mkdir(parents=True, exist_ok=True)

        # A place for third-party static libraries to be linked.
        self.static = self.root.joinpath("static")
        self.static.mkdir(parents=True, exist_ok=True)

        # A list of commands to run that should build dependencies.
        self.build_commands: List[List[str]] = []

        # Aggregate compiler flags.
        self.compile_flags = ["-iquote", str(self.include)]
        self.link_flags = [f"-L{self.static}"]

    def info(self, logger: LoggerType) -> None:
        """Log some information."""

        if self.build_commands:
            logger.info("Build commands: %s.", self.build_commands)
        logger.info("Third-party compile flags: %s.", self.compile_flags)
        logger.info("Third-party link flags: %s.", self.link_flags)

    def save(self, logger: LoggerType = None) -> None:
        """Save state data and create the third-party build script."""

        ARBITER.encode(self.state_path, self.state)
        if logger is not None:
            self.info(logger)

        script = self.root.joinpath("third_party.sh")
        with script.open("w") as script_fd:
            script_fd.write("#!/bin/bash\n\n")

            # Add build commands.
            for command in self.build_commands:
                script_fd.write(" ".join(command))
                script_fd.write("\n")

            script_fd.write("\ndate > $1\n")

        set_exec_flags(script)

    def _create_task(self, dep: Dependency) -> DependencyTask:
        """Create a new task object."""

        dep_data: DependencyData = self.state.setdefault(
            str(dep),
            {},
        )  # type: ignore

        return DependencyTask(
            self.root,
            self.include,
            self.static,
            self.build_commands,
            self.compile_flags,
            self.link_flags,
            dep,
            DependencyState(dep_data.setdefault("state", "init")),
            dep_data.setdefault("handler", {}),
            set(),
        )

    def audit(self, dep: Dependency) -> DependencyState:
        """Interact with a dependency if needed."""

        tasks = [self._create_task(dep)]
        resolved: Set[Dependency] = set()

        while tasks:
            task = tasks.pop()
            state = HANDLERS[dep.kind](task)
            resolved.add(task.dep)

            # Update state.
            task.data["state"] = str(state.value)

            # Handle any nested dependencies.
            #
            # Enable this soon!
            #
            # for nested in task.nested:
            #     if nested not in resolved:
            #         tasks.append(self._create_task(nested))

        return state
