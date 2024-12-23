from dataclasses import dataclass, field
from typing import Dict, Set, Any, Optional
from datetime import datetime

@dataclass
class PuzzleStep:
    """Represents a single step in a puzzle sequence"""
    step_id: str
    name: str
    description: str
    completed: bool = False
    required_items: Set[str] = field(default_factory=set)
    required_location: Optional[str] = None
    completed_at: Optional[str] = None
    custom_data: Dict[str, Any] = field(default_factory=dict)

    def complete(self) -> None:
        """Mark this step as completed"""
        self.completed = True
        self.completed_at = datetime.now().isoformat()

@dataclass
class PuzzleState:
    """Manages the state and progression of a puzzle"""
    puzzle_id: str
    current_step: int = 0
    completed: bool = False
    steps: Dict[str, PuzzleStep] = field(default_factory=dict)
    visited_locations: Set[str] = field(default_factory=set)
    collected_items: Set[str] = field(default_factory=set)
    custom_state: Dict[str, Any] = field(default_factory=dict)
    completed_at: Optional[str] = None

    def complete_step(self, step_id: str) -> None:
        """Mark a step as completed and update puzzle state"""
        if step_id in self.steps:
            self.steps[step_id].complete()
            # Check if this was the last step
            if all(step.completed for step in self.steps.values()):
                self.completed = True
                self.completed_at = datetime.now().isoformat()

    def get_current_step(self) -> Optional[PuzzleStep]:
        """Get the current active step"""
        for step in self.steps.values():
            if not step.completed:
                return step
        return None

    def check_requirements(self, location: str, inventory: Set[str]) -> bool:
        """Check if current step requirements are met"""
        current_step = self.get_current_step()
        if not current_step:
            return False

        # Check location requirement
        if current_step.required_location and current_step.required_location != location:
            return False

        # Check item requirements
        if not current_step.required_items.issubset(inventory):
            return False

        return True

    def serialize(self) -> dict:
        """Convert state to serializable format"""
        return {
            'puzzle_id': self.puzzle_id,
            'current_step': self.current_step,
            'completed': self.completed,
            'completed_at': self.completed_at,
            'steps': {
                step_id: {
                    'step_id': step.step_id,
                    'name': step.name,
                    'description': step.description,
                    'completed': step.completed,
                    'completed_at': step.completed_at,
                    'required_items': list(step.required_items),
                    'required_location': step.required_location,
                    'custom_data': step.custom_data
                }
                for step_id, step in self.steps.items()
            },
            'visited_locations': list(self.visited_locations),
            'collected_items': list(self.collected_items),
            'custom_state': self.custom_state
        }

    @classmethod
    def deserialize(cls, data: dict) -> 'PuzzleState':
        """Create a new state instance from serialized data"""
        steps = {
            step_id: PuzzleStep(
                step_id=step_data['step_id'],
                name=step_data['name'],
                description=step_data['description'],
                completed=step_data['completed'],
                completed_at=step_data['completed_at'],
                required_items=set(step_data['required_items']),
                required_location=step_data['required_location'],
                custom_data=step_data['custom_data']
            )
            for step_id, step_data in data['steps'].items()
        }

        return cls(
            puzzle_id=data['puzzle_id'],
            current_step=data['current_step'],
            completed=data['completed'],
            completed_at=data['completed_at'],
            steps=steps,
            visited_locations=set(data['visited_locations']),
            collected_items=set(data['collected_items']),
            custom_state=data['custom_state']
        ) 