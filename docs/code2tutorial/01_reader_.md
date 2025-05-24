# Chapter 1: Reader

Welcome to the first chapter of the Alt-Ctrl-Proj tutorial! In this chapter, we'll get started with the very first step in using the library: reading your Primavera P6 XER file.

Think of an XER file as a snapshot of your project schedule from Primavera P6. It contains all the details about your projects, activities (tasks), relationships, resources, calendars, and much more, all stored in a special format.

To do anything with this data using Alt-Ctrl-Proj, you first need to open this file and translate its contents into something Python can easily understand and work with. That's exactly what the `Reader` does!

## What is the Reader?

The `Reader` is your essential starting point in the Alt-Ctrl-Proj library. It's like a key that unlocks the data hidden inside your XER file.

Imagine you have a locked box (your XER file) filled with carefully organized project information. The `Reader` is the specialized tool designed to open that specific type of box. When you use the `Reader`, it goes through the XER file, reads all the bits of information, and then puts that information into structured Python objects that are much easier to access and manipulate than trying to read the raw text file yourself.

Your main goal in this chapter is to learn how to use the `Reader` to load your XER file and get access to the project data within it.

## Getting Started: Loading Your First XER File

Before we can use the `Reader`, we need to install the Alt-Ctrl-Proj library. If you haven't already, open your terminal or command prompt and run this command:

```bash
pip install Alt-Ctrl-Proj
```

This command downloads and installs the library on your computer.

Now, let's see the `Reader` in action. The very first thing you need to do in your Python script is import the `Reader` class:

```python
from xer_parser.reader import Reader
```

This line tells Python that you want to use the `Reader` tool from the library.

Next, you create an instance of the `Reader` class, providing the path to your XER file. Let's assume you have a file named `my_project.xer` in the same directory as your Python script.

```python
# Create a Reader object and load the file
xer = Reader("my_project.xer")
```

That single line, `xer = Reader("my_project.xer")`, does all the heavy lifting! It opens `my_project.xer`, reads its entire content, parses it, and creates a `Reader` object (we've named it `xer`) that holds all the project data neatly organized.

Now that you have the `xer` object, you have access to the project's data. A single XER file can sometimes contain data for multiple projects, though it's most common to see just one. The `Reader` object provides a way to get all the projects it found:

```python
# Access the projects loaded by the Reader
# .projects is a collection (more on this in the next chapter!)
for project in xer.projects:
    # We'll learn more about Project objects later, but let's print a key detail
    print(f"Loaded Project: {project.proj_short_name}")
```

**What this code does:**

1. `xer = Reader("my_project.xer")`: Creates the Reader and loads the file.
2. `xer.projects`: Accesses the 'projects collection' stored inside the `xer` object. This collection holds all the project details found in the file.
3. `for project in xer.projects:`: Loops through each individual project object in the collection.
4. `print(...)`: Prints a piece of information from each project object (specifically, its short name).

If your `my_project.xer` file contained one project named "My Awesome Project", the output might look something like this:

```text
Loaded Project: My Awesome Project
```

Success! You've just loaded an XER file and accessed basic information from it using the `Reader`.

## How Does the Reader Work? (Under the Hood)

You might be wondering, what magic happens inside that `Reader("my_project.xer")` line? Let's take a simplified look.

An XER file isn't just random text. It's structured into different sections, often referred to as "tables". Each section starts with `%T` followed by the table name (like `PROJECT` or `TASK`). Then comes a line starting with `%F` listing the 'fields' or column headers for that table. Finally, many lines starting with `%R` follow, each representing a single 'record' or row of data in that table.

The `Reader` opens the file and reads it line by line.

1. When it sees a line starting with `%T`, it notes down the name of the 'table' it's about to read data for.
2. When it sees a line starting with `%F`, it reads and remembers the names of the 'columns' for the current table.
3. When it sees a line starting with `%R`, it knows this is a data row for the current table. It matches the values in this row to the 'columns' it remembered from the `%F` line.

For every `%R` line it reads, the `Reader` intelligently decides what kind of Python object to create based on the current table name (`%T`). For example:

* If the table is `PROJECT`, it creates a `Project` object.
* If the table is `TASK`, it creates a `Task` object.
* If the table is `PROJWBS`, it creates a `WBS` object.
* ... and so on for all the different types of data in an XER file.

It then fills this new Python object with the data from the `%R` line and stores it in the appropriate place inside the `Reader` object itself. This is how `xer.projects` gets populated with `Project` objects, `xer.activities` with `Task` objects, and so on.

Here’s a very simplified sequence diagram showing this process:

```mermaid
sequenceDiagram
    participant User as User
    participant Reader as Reader object
    participant XERFile as XER File (my_project.xer)

    User->Reader: xer = Reader("my_project.xer")
    activate Reader
    Reader->XERFile: Open file
    XERFile-->Reader: File content streamed

    loop Read line by line
        Reader->XERFile: Read line
        alt Line is %T
            XERFile-->Reader: "%T PROJECT"
            Note over Reader: Identify current table: PROJECT
        alt Line is %F
            XERFile-->Reader: "%F proj_id\t..."
            Note over Reader: Store headers for PROJECT
        alt Line is %R
            XERFile-->Reader: "%R 1234\t..."
            Note over Reader: Read record data
            Reader->Reader: Create Project object from data
            Reader->Reader: Add Project object to .projects list
        end
    end
    Reader->XERFile: Close file
    deactivate Reader
    User-->Reader: xer object is ready
```

This process continues until the entire file is read. By the end, the `xer` object holds Python representations of all the data originally in the XER file, organized into accessible collections.

Looking briefly at the actual code in `xer_parser/reader.py`, the core logic is within the `__init__` method:

```python
# Inside the Reader class __init__ method
# ... (initial setup)
with codecs.open(filename, encoding="utf-8", errors="ignore") as tsvfile:
    stream = csv.reader(tsvfile, delimiter="\t")
    for row in stream:
        if row[0] == "%T":
            current_table = row[1]
        elif row[0] == "%F":
            current_headers = [r.strip() for r in row[1:]]
        elif row[0] == "%R":
            zipped_record = dict(zip(current_headers, row[1:], strict=False))
            # This line creates and stores the object!
            self.create_object(current_table, zipped_record)

# ... (rest of the __init__)
```

The `create_object` method then looks at `current_table` and uses `if/elif` statements to decide which collection (`self._projects`, `self._tasks`, etc.) to add the new object to.

## What Can You Access from the Reader?

Once you have the `xer` object (the instance of `Reader`), it acts as a container for all the different parts of your project data. The most important parts are exposed as attributes you can access directly:

* `.projects`: Contains all the project(s) found in the file. You'll learn more in [Chapter 3: Project](03_project_.md).
* `.activities`: Contains all the tasks or activities. We'll dive into this in [Chapter 4: Task (Activity)](04_task__activity__.md).
* `.wbss`: Holds the Work Breakdown Structure elements. See [Chapter 5: WBS (Work Breakdown Structure)](05_wbs__work_breakdown_structure__.md).
* `.relations`: Provides access to the relationships (dependencies) between tasks. This is covered in [Chapter 6: Relationship (TaskPred)](06_relationship__taskpred__.md).
* `.resources`: Contains information about resources used in the project. Learn more in [Chapter 7: Resource](07_resource_.md).
* `.calendars`: Contains project calendars.
* ... and many more collections for various Primavera P6 data types like Activity Codes, UDFs, etc.

Each of these attributes is a special collection object provided by Alt-Ctrl-Proj, designed to make it easy to find, filter, and work with the specific type of data it holds. We'll explore these collections in detail in the following chapters.

## Putting it All Together (A Slightly Bigger Example)

Let's combine what we've learned to load a file and list the first few activities in the main project.

```python
from xer_parser.reader import Reader

# 1. Load the XER file
file_path = "my_project.xer"
print(f"Attempting to load file: {file_path}")

try:
    xer = Reader(file_path)
    print("File loaded successfully!")

    # 2. Access the projects (assuming one main project)
    if xer.projects:
        main_project = xer.projects[0] # Get the first project
        print(f"\nExploring project: {main_project.proj_short_name}")

        # 3. Access the activities (tasks)
        activities = xer.activities # Get the activities collection
        print(f"Total activities found: {activities.count}")

        # 4. Print details for the first few activities
        print("\nFirst 5 activities:")
        # We'll learn how to iterate over collections easily in Chapter 2
        # For now, let's manually access the internal list if available
        activity_list = activities.activities[:5] # Get first 5 from internal list
        if activity_list:
            for i, activity in enumerate(activity_list):
                 # Accessing basic attributes like task_code and task_name
                 print(f"{i+1}. {activity.task_code} - {activity.task_name}")
        else:
            print("No activities found.")

    else:
        print("No projects found in the XER file.")

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

```

**What this code does:**

1. Imports the `Reader`.
2. Defines the file path and attempts to create a `Reader` object within a `try...except` block to handle potential errors like the file not existing.
3. Checks if any projects were loaded (`if xer.projects:`).
4. If projects exist, it grabs the first one (`main_project = xer.projects[0]`) and prints its name.
5. It accesses the activities collection (`activities = xer.activities`).
6. It prints the total number of activities found using `.count`.
7. It then accesses an internal list of activities within the collection (`activities.activities`) and takes the first 5 using slicing `[:5]`. This is a temporary way to show accessing data; we'll learn the standard way to iterate in the next chapter.
8. Finally, it loops through these first 5 activity objects and prints their code and name.

This example shows how the `Reader` object acts as the central hub, providing access to all the different types of project data once the file is loaded.

## Conclusion

In this chapter, you've learned that the `Reader` is the essential first step for working with Primavera P6 XER files in Alt-Ctrl-Proj. You import it, create an instance by giving it your XER file path, and it handles the complex task of parsing the file and organizing the data into accessible Python objects.

Once you have the `Reader` object, you can access various "collections" of data within it, such as projects, activities, WBS elements, and relationships.

Now that you know how to load your data, the next step is to understand how to effectively navigate and use these collections of objects.

Let's move on to [Chapter 2: Data Collections](02_data_collections_.md) to explore how the `Reader` organizes all that information and how you can start working with groups of objects like tasks or WBS elements.

---

<sub><sup>Generated by [AI Codebase Knowledge Builder](https://github.com/The-Pocket/Tutorial-Codebase-Knowledge).</sup></sub> <sub><sup>**References**: [[1]](https://github.com/osama-ata/Alt-Ctrl-Proj/blob/61f38213dc38bccd4d84cb765b1a5678723c47c2/README.md), [[2]](https://github.com/osama-ata/Alt-Ctrl-Proj/blob/61f38213dc38bccd4d84cb765b1a5678723c47c2/docs/source/examples.rst), [[3]](https://github.com/osama-ata/Alt-Ctrl-Proj/blob/61f38213dc38bccd4d84cb765b1a5678723c47c2/docs/source/getting_started.rst), [[4]](https://github.com/osama-ata/Alt-Ctrl-Proj/blob/61f38213dc38bccd4d84cb765b1a5678723c47c2/docs/source/tools.rst), [[5]](https://github.com/osama-ata/Alt-Ctrl-Proj/blob/61f38213dc38bccd4d84cb765b1a5678723c47c2/xer_parser/reader.py), [[6]](https://github.com/osama-ata/Alt-Ctrl-Proj/blob/61f38213dc38bccd4d84cb765b1a5678723c47c2/xer_parser/tools/explorer.py)</sup></sub>
