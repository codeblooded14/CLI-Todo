import sqlite3

sqlconnection = sqlite3.connect('todo.db')
dbCursor = sqlconnection.cursor()

# def pintthewholegoddamnthing():
#     full = dbCursor.execute('''SELECT * FROM TASK''').fetchall()
#     for i in full:
#         print(i)


def completedTasks():
    dbCursor.execute("""SELECT Task_Name FROM TASK WHERE Completed_Status = 'True'""")
    completedTaskList  = dbCursor.fetchall()
    if len(completedTaskList) == 0:
        print('No Completed tasks, push harder!')
        homePage()
    else:
        print("Task No","\t","Completed Tasks")
        for index,tasks in enumerate(completedTaskList,1):
            print(index, ".\t",tasks[0])

    print("""\nType the corresponding number/command for desired function
            1 --> Delete Task Permanently
            2 --> Push Task to Pending tasks
            'home' --> for homepage""")

    completedNav = input('Enter option: ')
    if completedNav.isdigit():
        if completedNav == '1':
            tasknoDel = input('Enter Task No: ')
            if tasknoDel.isdigit() and int(tasknoDel) <= len(completedTaskList):
                dbCursor.execute("DELETE FROM TASK WHERE Task_Name = '{}'".format(completedTaskList[int(tasknoDel) - 1][0]))
                sqlconnection.commit()
                completedTasks()
            else:
                print('Invalid Input, going Back to Home Page')
                homePage()
        elif completedNav == '2':
            tasknoPush = input('Enter Task no: ')
            if tasknoPush.isdigit() and int(tasknoPush) <= len(completedTaskList):
                dbCursor.execute("UPDATE TASK SET Pending_Status = '{}', Completed_Status = '{}' WHERE Task_Name = '{}';".format('True','False',completedTaskList[int(tasknoPush) - 1][0]))
                sqlconnection.commit()
                completedTasks()
            else:
                print('Invalid Input, going Back to HomePage')
                homePage()
        else:
            print('Invalid Input, going Back to Home Page')
            homePage()
    else:
        if completedNav == 'home':
            homePage()
        else:
            print('Invalid Input')
            completedTasks()

def pendingTasks():
    dbCursor.execute("""SELECT Task_Name FROM TASK WHERE Pending_Status = 'True'""")
    pendingTaskList  = dbCursor.fetchall()
    if len(pendingTaskList) == 0:
        print('Hooray! No pending tasks')
        homePage()
    else:
        print("Task No","  ","Pending Tasks")
        for index,tasks in enumerate(pendingTaskList,1):
            print(index, ".\t",tasks[0])

    print("""\nType the corresponding number/command for desired function
                1 --> Delete Task Permanently
                2 --> Push Task to Completed tasks
                'home' --> for homepage""")


    pendingNav = input('Enter option: ')
    if pendingNav.isdigit():
        if pendingNav == '1':
            tasknoDel = input('Enter Task No: ')
            if tasknoDel.isdigit() and int(tasknoDel) <= len(pendingTaskList):
                dbCursor.execute("DELETE FROM TASK WHERE Task_Name = '{}'".format(pendingTaskList[int(tasknoDel) - 1][0]))
                sqlconnection.commit()
                pendingTasks()
            else:
                print('Invalid Input, going Back to Home Page')
                homePage()
        elif pendingNav == '2':
            tasknoPush = input('Enter Task no: ')
            if tasknoPush.isdigit() and int(tasknoPush) <= len(pendingTaskList):
                dbCursor.execute("UPDATE TASK SET Completed_Status = '{}',Pending_Status = '{}' WHERE Task_Name = '{}';".format('True','False', pendingTaskList[int(tasknoPush) - 1][0]))
                sqlconnection.commit()
                pendingTasks()
            else:
                print('Invalid Input, going Back to Home Page')
                homePage()
        else:
            print('Invalid Input, going Back to Home Page')
            homePage()
    else:
        if pendingNav == 'home':
            homePage()
        else:
            print('Invalid Input')
            pendingTasks()

def addTask():
    while True:
        taskName = input('Enter New Task/Event: ')

        dbCursor.execute(""" INSERT INTO TASK VALUES ('{}','{}','{}')""".format(taskName,'True','False'))
        sqlconnection.commit()

        continueThresh = input('Do you want to add more? y/n ')
        if continueThresh == 'n' or continueThresh == 'N':
            homePage()
            break
        elif continueThresh == 'Y' or continueThresh == 'y':
            pass
        else:
            print("Invalid Input, I'll take it as a no")
            homePage()
            break


def homePage():
    print(''' 
    Welcome to To-do CLI program

    Choose the serial number to navigate to 
    the corresponding function.

                1 --> View Pending tasks
                2 --> View Completed tasks
                3 --> Add new task
    
    Enter 'exit' to exit the application
                
                ''')
    navigateVal = input("Enter 'exit' or Serial no: ")
    if navigateVal == '1':
        pendingTasks()
    elif navigateVal == '2':
        completedTasks()
    elif navigateVal == '3':
        addTask()
    elif navigateVal == 'exit':
        exit()
    else:
        print('Invalid Command')
        homePage()

tableCommand = """ 
    CREATE TABLE IF NOT EXISTS TASK (
        Task_Name VARCHAR(500) NOT NULL,
        Pending_Status CHAR(25) NOT NULL,
        Completed_Status CHAR(25) NOT NULL
        );"""
dbCursor.execute(tableCommand)
homePage()