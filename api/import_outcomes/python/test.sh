#!/usr/bin/env sh
#nosetests --cover-html tests#
nosetests tests.test_importer:OutcomeImporterTests  --with-coverage --cover-html --cover-html-dir=coverage_output
