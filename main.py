from bakery import assert_equal
from drafter import *
from dataclasses import dataclass
import random

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
class scheduledCourse:
    course: Course
    days: str
    startTime: int
    duration: float
    
@dataclass
class timeBlock:
    day: str
    startTime: int
    duration: int

@dataclass
class State:
    courseList: list[Course]               # A list of courses that is added to when the user is on the required courses page.
    timeBlocks: list[timeBlock]            # A list of times that should not include any classes. This is altered in the time blocks page.
    userNotes: list[str]                   # A list of strings that the user adds to from the user notes page.
    completedNotes: list[bool]             # A list of booleans that correspond to the index of user notes that have already been written.
    currentSchedule: list[scheduledCourse] # A list of instances of a Course in order. (May need to add a sub-class that includes the chosen time)

@route
def index(state: State) -> Page:
    return Page(state, [
                Header("Welcome to Schedule Builder!"),
                Button("Add Courses", "addCourse"),
                Button("Add Time Blocks", "addTimeBlock"),
                Button("Schedule", "makeSchedule"),
                Button("Notes", "addNote"),
                ])

@route
def createTimeBlock(state: State, day: str, start: str, end: str) -> Page:
    startTime = convertToMinutes(start)
    endTime = convertToMinutes(end)
    if startTime >= endTime:
        return Page(state, [
            Header("Invalid Time Block"),
            Text("The end time must be later than the start time."),
            Button("Go Back", "addTimeBlock")
        ])
    duration = endTime - startTime
    state.timeBlocks.append(
        timeBlock(day, startTime, duration)
    )
    return addTimeBlock(state)

def convertToMinutes(time: str) -> int:
    parts = time.split()
    hourMinute = parts[0].split(":")
    hour = int(hourMinute[0])
    minute = int(hourMinute[1])
    period = parts[1]
    if period == "PM" and hour != 12:
        hour += 12
    elif period == "AM" and hour == 12:
        hour = 0
    return hour * 60 + minute

@route
def addTimeBlock(state: State) -> Page:
    timeOptions = [
        formatTime(time)
        for time in range(8 * 60, 17 * 60 + 1, 30)
    ]
    components = [
        Header("Time Blocks"),
        Text("Select days and times when you do not want classes."),
        LineBreak(),
        Text("Day:"),
        SelectBox("day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]),
        "Start Time:",
        SelectBox("start", timeOptions),
        "End Time:",
        SelectBox("end", timeOptions),
        LineBreak(),
        Button("Add Time Block", "createTimeBlock"),
        LineBreak(),
        Header("Your Current Time Blocks")
    ]
    for index, block in enumerate(state.timeBlocks):
        endTime = block.startTime + block.duration
        components.append(
            Text(block.day + ": " + formatTime(block.startTime)
                 + " - " + formatTime(endTime))
        )
        components.append(
            Button("Remove", "removeTimeBlock", arguments={"index": index})
        )
        components.append(LineBreak())
    components.extend([
        Button("Home", "index"),
        Button("Courses", "addCourse"),
        Button("Schedule", "makeSchedule"),
        Button("Notes", "addNote")
    ])
    return Page(state, components)

@route
def removeTimeBlock(state: State, index: int) -> Page:
    state.timeBlocks.pop(index)
    return addTimeBlock(state)

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
                    Button("Schedule", "makeSchedule"),
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
def overlaps(start1: int, duration1: int, start2: int, duration2: int) -> bool:
    return start1 < start2 + duration2 and start2 < start1 + duration1
def formatTime(minutes: int) -> str:
    hour = minutes // 60
    minute = minutes % 60
    period = "AM" if hour < 12 else "PM"
    if hour > 12:
        hour -= 12
    if hour == 0:
        hour = 12
    return str(hour) + ":" + str(minute).zfill(2) + " " + period

@route
def makeSchedule(state: State) -> Page:
    state.currentSchedule = []
    unscheduled = []
    courses = state.courseList.copy()
    random.shuffle(courses)
    patterns = [
        ("MWF", ("Monday", "Wednesday", "Friday")),
        ("TR", ("Tuesday", "Thursday"))
    ]
    for course in courses:
        placed = False
        coursePatterns = patterns.copy()
        random.shuffle(coursePatterns)

        for days, actualDays in coursePatterns:
            if days == "MWF":
                duration = int(course.durationMWF * 60)
            else:
                duration = int(course.durationTR * 60)
            possibleTimes = list(range(8 * 60, 17 * 60, 30))
            random.shuffle(possibleTimes)

            for startTime in possibleTimes:
                conflict = False
                for block in state.timeBlocks:
                    if block.day in actualDays:
                        if overlaps(startTime, duration,
                                   block.startTime, block.duration):
                            conflict = True
                            break
                if not conflict:
                    for scheduled in state.currentSchedule:
                        sharedDays = any(
                            day in scheduled.days for day in days
                        )
                        if sharedDays:
                            if overlaps(startTime, duration,
                                       scheduled.startTime,
                                       scheduled.duration):
                                conflict = True
                                break
                if not conflict:
                    state.currentSchedule.append(
                        scheduledCourse(course, days, startTime, duration)
                    )
                    placed = True
                    break
            if placed:
                break
        if not placed:
            unscheduled.append(course.title)
    rows = []
    daysOfWeek = [
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
    ]
    dayCodes = {
        "Monday": "M",
        "Tuesday": "T",
        "Wednesday": "W",
        "Thursday": "R",
        "Friday": "F"
    }
    for startTime in range(8 * 60, 17 * 60, 30):
        row = [formatTime(startTime)]
        for day in daysOfWeek:
            cell = ""
            for scheduled in state.currentSchedule:
                if dayCodes[day] in scheduled.days:
                    if startTime == scheduled.startTime:
                        cell = scheduled.course.title
                        break
                    elif (startTime > scheduled.startTime and
                          startTime < scheduled.startTime + scheduled.duration):
                        cell = "↳"
                        break
            if cell == "":
                for block in state.timeBlocks:
                    if block.day == day:
                        if overlaps(startTime, 30,
                                   block.startTime, block.duration):
                            cell = "Blocked"
                            break
            row.append(cell)
        rows.append(row)
    table = Table(
        rows,
        ["Time", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    )
    components = [
        Header("Your Schedule"),
        table
    ]
    if unscheduled:
        components.append(Header("Courses That Couldn't Be Scheduled"))
        for course in unscheduled:
            components.append(Text(course))
    components.extend([
        Button("Randomize Again", "makeSchedule"),
        Button("Home", "index"),
        Button("Courses", "addCourse"),
        Button("Time Blocks", "addTimeBlock"),
        Button("Notes", "addNote")
    ])
    return Page(state, components)

start_server(State([], [], [], [], []))
