#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 14:56:17 2023

"""
# maybe replace by machine.timer...

import time

class Timer:
    def __init__(self, max_delay):
        self.max_delay = max_delay
        self.delay = 0
        self.start_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.delay = 0
        self.start_time = 0

    def check(self):
        if self.start_time == 0:
            return False

        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.max_delay:
            self.start_time = 0
            return True
        else:
            return False
