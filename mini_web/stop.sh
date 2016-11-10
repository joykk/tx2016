#!/bin/bash


kill `ps -ef | grep "python app" | grep -v "grep" | awk '{print $2}'`
