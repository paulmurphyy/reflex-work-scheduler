import reflex as rx
from .base_state import State
from typing import Dict, List
from .availability_state import availabilityState
from models import Availability, Employee

class calendarState(State):
    #Properties:
    heatmap: Dict[str, dict[int, int]] = {}
    days: List[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hours: List[int] = [9, 10, 11, 12, 13, 14, 15, 16]

    #Calculated Properties:
    @rx.var
    def max_emp_count(self) -> int:
        """
        Helper that determines how 'dark' the green should be.
        """
        return max([max(d.values()) for d in self.heatmap.values()] or [1])

    #Functions:
    def update_heatmap(self):
        """
        Intakes from the DB, calculating the sums.
        """
        #Init empty grid:
        grid_count = {day: {h: 0 for h in self.hours} for day in self.days}

        with rx.session() as session:
            #Pull everyone's availability:
            all_avals = session.scalars(Availability.select()).all()

            #Create records for the data:
            for record in all_avals:
                for day, active_hours in record.availability.items():
                    for h in active_hours:
                        if day in grid_count and h in grid_count[day]:
                            grid_count[day][h] += 1

        #Update heatmap with new grid status:
        self.heatmap = grid_count

        



    