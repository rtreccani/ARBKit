#click library for defining CLI options and arguements etc..
import click

#overarching group to define the entrypoint of the program and placehold for the sub-commands defined below
@click.group()
#no args, params, etc.. no content either. placeholder.
def cli():
    pass 

#click setup for load command, mandatory filename arguement. 
@cli.command()
@click.argument('filename')
def load(filename):
    click.echo('loading the file: ' + str(filename))

#click setup for play command, optional delay value
@cli.command()
@click.option('--delay', default=0.0, help='time between command and playback beginning')
def play(delay):
    click.echo('playing with delay '+str(delay))

#click pause command
@cli.command()
def pause():
    click.echo('pausing playback')

#click connect, mandatory port, optional baud rate. 
@cli.command()
@click.argument('port')
@click.option('--baud', default=115200, help='bit rate to communicate at')
def connect(port, baud):
    click.echo('connecting to port '+str(port)+' at baud '+str(baud))


#add all the commands to the overarching group. 
cli.add_command(load)
cli.add_command(play)
cli.add_command(pause)
cli.add_command(connect)

#setuptools takes care of the entrypoint stuff.