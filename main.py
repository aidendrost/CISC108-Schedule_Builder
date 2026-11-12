from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

set_website_framed(False)
hide_debug_information()
set_website_title("Schedule Builder")
set_site_information(author = "Aiden Drost",
                     description = "",
                     sources = "",
                     planning = "",
                     links = ["https://github.com/aidendrost/CISC108-Schedule_Builder/"]
                    )

@dataclass
class Course:
    title: str
    creditHours: int
    durationMWF: int
    durationTR: int

@dataclass
class State:
    courseList: list[Course]      # A list of courses that is added to when the user is on the required courses page.
    timeBlocks: list[int]         # A list of times that should not include any classes. This is altered in the time blocks page.
    userNotes: list[str]          # A list of strings that the user adds to from the user notes page.
    currentSchedule: list[Course] # A list of instances of a Course in order. (May need to add a sub-class that includes the chosen time)

@route
def index(state: State) -> Page:
    return Page(state, [
                Header("Welcome to Schedule Builder!"),
                Button("Add Time Blocks", "addTimeBlock"),
                Button("Notes", "addNote"),
                ])


@route
def addTimeBlock(state: State) -> Page:
    return Page(state, [
                Header("Select times where classes should not be planned."),
                Button("", ""),
                Button("", ""),
                ])

@route
def removeTimeBlock(state: State) -> Page:
    pass

@route
def addCourse(state: State) -> Page:
    return Page(state, [
                Header("Add your courses below!"),
                ])

@route
def removeCourse(state: State) -> Page:
    pass

@route
def addNote(state: State) -> Page:
    return Page(state, [
                Header("Notes"),
                Button("", ""),
                Button("", ""),
                ])

@route
def toggleNote(state: State) -> Page:
    pass

@route
def removeNote(state: State) -> Page:
    pass

@route
def makeSchedule(state: State) -> Page:
    pass



start_server()
