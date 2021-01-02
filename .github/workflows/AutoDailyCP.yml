#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# https://github.com/lemofire/AutoDailyCP
# Lisence: MIT
# Author: 柠火
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

name: AutoDailyCP

on:
  push:
    branches: 
      - master
  watch:
    types: started
  schedule:
    - cron: 0,30 4,5 * * *

jobs:
  build:
    runs-on: ubuntu-latest
    if: github.event.repository.owner.id == github.event.sender.id
    steps:
      - name: Checkout
        uses: actions/checkout@master
      - name: Install python3
        run: |
          sudo -E apt-get -yqq update
          sudo -E apt-get -yqq install python3
      - name: Install extensions
        run: |
          pip3 install setuptools
          pip3 install -r requirements.txt
      - name: Run program
        env:
          SCHOOL_NAME: ${{ secrets.SCHOOL_NAME }}
          ACCOUNT: ${{ secrets.ACCOUNT }}
          PASSWORD: ${{ secrets.PASSWORD }}
          ADDRESS: ${{ secrets.ADDRESS }}
        run: |
          python3 DailyCP.py ${SCHOOL_NAME} ${ACCOUNT} ${PASSWORD} ${ADDRESS} formdb
      - name : Upload formdb
        uses: actions/upload-artifact@master
        with:
          name: formdb
          path: formdb
