import serial, Queue, threading, subprocess, string

"""
	1.Implementation to receive gesture input over Arduino serial port
    2.Translate the input to commands for pianobar
    Author Hanumant Singh
"""


class gesture_Thread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
        self.signal = True
        self.daemon = True
    def run(self):
        print "Starting gesture thread " + self.name
        get_gesture(self.q, self.signal)
        print "Exiting gesture Thread" + self.name

class painobar_Thread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.daemon = True
    def run(self):
        print "Starting pianobar thread"
        subprocess.call("pianobar", shell=True)
        print "Exiting pianobar thread"

def get_gesture(q, signal):
	ser = serial.Serial("/dev/cu.usbmodem1411", 9600);
	if (ser):
		print("Serial port" + ser.portstr + " opened")
	while signal:
		gesture = ser.readline()
		com_q_lock.acquire()
		if q.full():
			print("Communication queue full dropping gesture" + gesture)
		else:
			q.put(gesture);
		com_q_lock.release()

state = "init"

# Determine if pianobar needs to be started
while True:
	print("Do you need to start pandora? Y/N")
	answer = raw_input()
	if answer == 'N':
		break
	elif answer == 'Y':
		pianobar = painobar_Thread("2", "pianobar")
		pianobar.start()
		break		
	else:
		print("Invalid input")

state = "playing"		
comm_q = Queue.Queue(2);
com_q_lock = threading.Lock()

# Create thread to get gesture
gest_thread = gesture_Thread("1", "APDS_gesture", comm_q)
gest_thread.start()

# Translate incoming gesture to commands for pianobar
while True:
	com_q_lock.acquire()
	while not comm_q.empty():
		command = str(comm_q.get())
		if 'RIGHT' in command:
			print("Choosing next song")
			subprocess.call("echo n > /Users/Gunners/.config/pianobar/ctl", shell=True)
		elif 'UP' in command:
			print("Loving the song")
			subprocess.call("echo + > /Users/Gunners/.config/pianobar/ctl", shell=True)
		elif 'DOWN' in command:
			print("Hate the song")
			subprocess.call("echo - > /Users/Gunners/.config/pianobar/ctl", shell=True)
		elif 'FAR' in command:
			print("Quitting Pandora")
			subprocess.call("echo q > /Users/Gunners/.config/pianobar/ctl", shell=True)
			gest_thread.signal = False
			state = "stopped"
			com_q_lock.release()
			break
		elif 'NEAR' in command:
			if state == "playing":
				print ("Pausing song")
				subprocess.call("echo p > /Users/Gunners/.config/pianobar/ctl", shell=True)
				state = "paused"
			else:
				print ("Resuming song")
				subprocess.call("echo P > /Users/Gunners/.config/pianobar/ctl", shell=True)
				state = "playing"
		elif 'NONE' in command:
			print("Repeat Gesture")
		else:
			print("")
	if 'stopped' not in state:
		com_q_lock.release()
	else:
		break


