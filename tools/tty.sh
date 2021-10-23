#!/bin/bash

ls -l /dev/tty* | grep dialout | grep -v /dev/ttyS
