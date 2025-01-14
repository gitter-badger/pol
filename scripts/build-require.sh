#!/usr/bin/env bash
set -ex

pip-compile --no-index ./requirements/dev.in

pip-compile --no-index ./requirements/prod.in

pip-sync requirements/*.txt docs/requirements.txt
