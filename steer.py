#!/usr/bin/env python3
from configparser import ConfigParser
import paho.mqtt.client as mqtt
import pygame
import time

#configuration
config = ConfigParser()
with open( "steer.conf",'r') as f:
    config.read_file(f)

class updater():
    def __init__(self, m):
        self.mqtt = m
        self.state = {
        }

    def update(self):
        for key, value in self.state.items():
            self.mqtt.publish(f"{publishTopic}/{key}", value)


#mqtt
publishTopic = config.get( "mqtt", "publishTopic")
c = mqtt.Client()
c.connect( config.get( "mqtt", "host"), config.getint( "mqtt", "port"))

u = updater(c)

#setup window and graphics
view = [ 800, 600]

pygame.init()
screen = pygame.display.set_mode(view)

mb = False
run = True
ntime = time.time()
while run:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_w:
                u.state.update({
                    "spd":30
                    })

            elif event.key == pygame.K_s:
                u.state.update({
                    "spd":-30
                    })

            elif event.key == pygame.K_a:
                u.state.update({
                    "dir":40
                    })

            elif event.key == pygame.K_d:
                u.state.update({
                    "dir":-40
                    })

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_a:
                u.state.update({
                    "dir":0
                    })
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                u.state.update({
                    "spd":0
                    })

        elif event.type == pygame.MOUSEBUTTONDOWN:
                mb = True

        elif event.type == pygame.MOUSEBUTTONUP:
                mb = False

        elif event.type == pygame.MOUSEMOTION and mb:
            pos = pygame.mouse.get_pos()
            u.state.update({
                "yaw" : -int(255*(pos[0]/view[0]-0.5)),
                "pitch" : -int(255*(pos[1]/view[1]-0.5))
            })

    print(u.state)
    if ntime < time.time():
        u.update()
        ntime = time.time()+0.1

    pygame.display.flip()

#cleanup
pygame.display.quit()
pygame.quit()
