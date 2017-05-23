#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import pygame
import httplib
import datetime
import xml.dom.minidom as dom

os.putenv('SDL_FBDEV', '/dev/fb1')


pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((480, 320))
font = pygame.font.Font('mono.ttf', 100)
font2 = pygame.font.Font('mono.ttf', 24)

def get_temp(location='Sweden/Stockholm/Tullinge'):
    c = httplib.HTTPSConnection('www.yr.no')
    c.connect()
    c.request('GET', 'https://www.yr.no/place/%s/forecast.xml' % location)
    r = c.getresponse()
    d = r.read()
    c.close()
    xml = dom.parseString(d)
    return (xml
            .getElementsByTagName('weatherdata')[0]
            .getElementsByTagName('forecast')[0]
            .getElementsByTagName('time')[0]
            .getElementsByTagName('temperature')[0]
            .getAttribute('value'))

def render_temp(location, temp, offset):
    text = font2.render(u'%s%s' % (location, temp), True, (255, 255, 255))
    rect = text.get_rect(center=(300, offset))
    lcd.blit(text, rect)

tempT = u'%s°C' % get_temp('Sweden/Stockholm/Tullinge')
tempS = u'%s°C' % get_temp('Sweden/Stockholm/Stockholm')

while True:
    t = datetime.datetime.now()

    text = font.render(t.strftime('%H:%M'), True, (255, 255, 255))
    rect = text.get_rect(center=(240, 160))
    if (t.minute % 5) == 0 and t.second == 0:
        try:
            tempT = u'%s°C' % get_temp('Sweden/Stockholm/Tullinge')
            tempS = u'%s°C' % get_temp('Sweden/Stockholm/Stockholm')
        except:
            tempT = u'E'
            tempS = u'E'
    lcd.fill((0, 0, 0))
    pygame.display.update()
    render_temp(u'Stockholm: ', tempS, 40)
    render_temp(u'Tullinge:  ', tempT, 65)
    lcd.blit(text, rect)
    pygame.display.update()
    time.sleep(0.5)

    text = font.render(t.strftime('%H %M'), True, (255, 255, 255))
    rect = text.get_rect(center=(240, 160))
    lcd.fill((0, 0, 0))
    pygame.display.update()
    render_temp(u'Stockholm: ', tempS, 40)
    render_temp(u'Tullinge:  ', tempT, 65)
    lcd.blit(text, rect)
    pygame.display.update()
    time.sleep(0.5)
