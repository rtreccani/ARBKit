import click

@click.group()
def cli():
    pass

#click setup for load command, must contain filename
@cli.command()
@click.argument('filename')
def load(filename):
    click.echo('loading the file: ' + str(filename))

@cli.command()
@click.option('--delay', default=0.0, help='time between command and playback beginning')
def play(delay):
    click.echo('playing with delay '+str(delay))

@cli.command()
def pause():
    click.echo('pausing playback')

@cli.command()
@click.argument('port')
@click.option('--baud', default=115200, help='bit rate to communicate at')
def connect(port, baud):
    click.echo('connecting to port '+str(port)+' at baud '+str(baud))



cli.add_command(load)
cli.add_command(play)
cli.add_command(pause)
cli.add_command(connect)