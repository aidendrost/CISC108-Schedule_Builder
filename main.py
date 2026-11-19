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
    durationMWF: float
    durationTR: float

@dataclass
class State:
    courseList: list[Course]      # A list of courses that is added to when the user is on the required courses page.
    timeBlocks: list[int]         # A list of times that should not include any classes. This is altered in the time blocks page.
    userNotes: list[str]          # A list of strings that the user adds to from the user notes page.
    completedNotes: list[bool]    # A list of booleans that correspond to the index of user notes that have already been written.
    currentSchedule: list[Course] # A list of instances of a Course in order. (May need to add a sub-class that includes the chosen time)

@route
def index(state: State) -> Page:
    return Page(state, [
                Header("Welcome to Schedule Builder!"),
                Button("Add Courses", "addCourse"),
                Button("Add Time Blocks", "addTimeBlock"),
                Button("Notes", "addNote"),
                ])


@route
def addTimeBlock(state: State) -> Page:
    return Page(state, [
                Header("Select times where classes should not be planned."),
                Button("Schedule", "makeSchedule"),
                Button("Courses", "addCourse"),
                Button("Notes", "addNote")
                ])

@route
def removeTimeBlock(state: State) -> Page:
    pass

@route
def createCourse(state: State, title: str, creditHours: int) -> Page:
    state.courseList.append(Course(title, creditHours, 1.0, 1.5))
    return addCourse(state)

@route
def addCourse(state: State) -> Page:
    components = []
    components.extend([
                    Header("Add your courses below."),
                    TextBox("title", "Course Title"),
                    TextBox("creditHours", "Credit Hours"),
                    Button("Submit", "createCourse"),
                    LineBreak()
                    ])
    for index, course in enumerate(state.courseList):
        components.append(Text("Course: " + course.title + ", " + str(course.creditHours) + " credit hours"))
        components.append(Button("Remove", "removeCourse", arguments={"index": index}))
        components.append(LineBreak())
    components.extend([
                    Button("Home", "index"),
                    Button("Time Blocks", "addTimeBlock"),
                    Button("Notes", "addNote")
                    ])
    return Page(state, components)

@route
def removeCourse(state: State, index: int) -> Page:
    state.courseList.pop(index)
    return addCourse(state)

@route
def createNote(state: State, note: str) -> Page:
    state.userNotes.append(note)
    state.completedNotes.append(False)
    return addNote(state)

@route
def addNote(state: State) -> Page:
    components = []
    components.extend([
                    Header("Notes"),
                    TextArea("note", "New note..."),
                    Button("Submit", "createNote"),
                    LineBreak()
                    ])
    for index, note in enumerate(state.userNotes):
        components.append(RelatedCheckBox("completed", str(index), default_value=state.completedNotes[index]))
        components.append(Text(note))
        components.append(Button("Remove", "removeNote", arguments={"index": index}))
        components.append(LineBreak())
    components.extend([
                    Button("Save Changes", "toggleNote"),
                    LineBreak(),
                    Button("Home", "index"),
                    Button("Courses", "addCourse"),
                    Button("Schedule", "makeSchedule"),
                    LineBreak()
                    ])
    return Page(state, components)

@route
def toggleNote(state: State, completed: list[str] = []) -> Page:
    for index in range(len(state.userNotes)):
        state.completedNotes[index] = str(index) in completed
    return addNote(state)

@route
def removeNote(state: State, index: int) -> Page:
    state.userNotes.pop(index)
    state.completedNotes.pop(index)
    return addNote(state)

@route
def makeSchedule(state: State) -> Page:
    pass



start_server(State([], [], [], [], []))
