#!/usr/bin/env python


`python main.py`


while [ $? -ne 0 ]

do
	 echo 'Restarting Bot...'

	 `python main.py`

done
