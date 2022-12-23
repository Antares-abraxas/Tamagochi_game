import pytest
import tamagotchi

app = TamagotchiWindow()

def test_sleep():
    app.sleeping = False
    assert app.sleep_test == True
    
def test_ambulance_Click():
    app.self_sleeping = False
    app.ambulance_Click()
    assert app.ambulance == True

def test_feed_Click():
    app.self_sleeping = False
    app.feed_Click()
    assert app.eating == True

def test_play_Click():
    app.self_sleeping = False
    app.play_Click()
    assert app.playing == True

def test_walk_Click():
    app.self_sleeping = False
    app.walk_Click()
    assert app.walking == True

def test_stop_Click():
    app.self_sleeping = False
    app.stop_Click()
    assert app.imageList == app.dinoImages

def test_animation_timer():
    index = app.imageIndex
    app.animation_timer
    assert index == app.imageIndex

def test_tick_timer():
    myapp.time_cycle = 60
    myapp.tick_timer 
    assert myapp.time_cycle == 0

def test_tick_timer1():
    app.hunger = 10 
    app.tick_timer
    assert app.hunger == 8

def test_tick_timer2():
    app.hunger = -5
    app.tick_timer
    assert app.hunger == 0

def test_tick_timer3():
    app.health = 10
    app.tick_timer
    assert app.health == 8

def test_tick_timer4():
    app.health = -5
    app.tick_timer
    assert app.health == 0
    
def test_tick_timer5():
    app.happiness = 10
    app.tick_timer
    assert app.happiness == 8

def test_tick_timer6():
    app.happiness = -5
    app.tick_timer
    assert app.happiness == 0

