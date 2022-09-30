#!/usr/bin/env python3
from configparser import ConfigParser
import paho.mqtt.client as mqtt
import pygame

#configuration
config = ConfigParser()
with open( "steer.conf",'r') as f:
    config.read_file(f)

#mqtt
publishTopic = config.get( "mqtt", "publishTopic")
c = mqtt.Client()
c.connect( config.get( "mqtt", "host"), config.getint( "mqtt", "port"))

#setup window and graphics
view = [ 800, 600]

pygame.init()
screen = pygame.display.set_mode(view)

mb = False
run = True
while run:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_w:
                c.publish(f"{publishTopic}/spd", 30)

            elif event.key == pygame.K_s:
                c.publish(f"{publishTopic}/spd", -30)

            elif event.key == pygame.K_a:
                c.publish(f"{publishTopic}/dir", 30)

            elif event.key == pygame.K_d:
                c.publish(f"{publishTopic}/dir", -30)

        elif event.type == pygame.MOUSEBUTTONDOWN:
                mb = True

        elif event.type == pygame.MOUSEBUTTONUP:
                mb = False

        elif event.type == pygame.MOUSEMOTION and mb:
            pos = pygame.mouse.get_pos()
            dirs = {
                "yaw" : -int(255*(pos[0]/view[0]-0.5)),
                "pitch" : -int(255*(pos[1]/view[1]-0.5))
            }
            for key, value in dirs.items():
                c.publish(f"{publishTopic}/{key}", value)
            
    pygame.display.flip()

#cleanup
pygame.display.quit()
pygame.quit()
