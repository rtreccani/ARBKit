#click library for defining CLI options and arguements etc..
import click
import os 
import time


#overarching group to define the entrypoint of the program and placehold for the sub-commands defined below
@click.group()
@click.version_option() #allows for --version to return auto-extracted info from setuptools 
#no args, params, etc.. no content either. placeholder.
def cli():
    pass #modern day equivalent of goto but whatever

#click setup for start command to spin up a serial manager process 
@cli.command
def startDaemon()

#click setup for load command, mandatory filename arguement. 
@cli.command()
@click.argument('filename', type=click.Path(exists=True))
def load(filename):
    click.echo("loading " + click.format_filename(filename))
    fileSizeBytes = os.path.getsize(filename)
    filestream = open(filename, 'rb')
    with click.progressbar(length=fileSizeBytes, label='Blitting ' + filename + ' to device') as progBar:
        progBar.update(0)
        while True:
            index = filestream.tell()
            a=filestream.read(1)
            if(not a):
                break
            time.sleep(0.001)
            if(index%100 ==0):
                progBar.update(index)
    print("done")

#click setup for play command, optional delay value
@cli.command()
@click.option('--mode', '-m', default='oneshot', type=click.Choice(['oneshot', 'loopn', 'loopinf'], case_sensitive=False))
@click.option('--delay', '-d', default=0, help='time between command and playback beginning')
def play(delay, mode):
    if(delay != 0): #only print delay if it's meaningful
        click.echo("delay = " + str(delay))
    click.echo("mode = " + str(mode))
    click.echo("playing")

#click pause command
@cli.command()
def pause():
    click.echo('pausing playback')

#click connect, mandatory port, optional baud rate. 
@cli.command()
@click.argument('port')
@click.option('--baud', '-b', default=115200, help='bit rate to communicate at')
def connect(port, baud):
    click.echo('connecting to port '+str(port)+' at baud '+str(baud))


#add all the commands to the overarching group. 
cli.add_command(load)
cli.add_command(play)
cli.add_command(pause)
cli.add_command(connect)

#setuptools takes care of the entrypoint stuff.