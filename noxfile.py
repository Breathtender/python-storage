# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Generated by synthtool. DO NOT EDIT!

from __future__ import absolute_import
import os
import shutil

import nox


BLACK_VERSION = "black==19.10b0"
BLACK_PATHS = ["docs", "google", "tests", "noxfile.py", "setup.py"]

DEFAULT_PYTHON_VERSION = "3.8"
SYSTEM_TEST_PYTHON_VERSIONS = ["2.7", "3.8"]
UNIT_TEST_PYTHON_VERSIONS = ["2.7", "3.6", "3.7", "3.8", "3.9"]
CONFORMANCE_TEST_PYTHON_VERSIONS = ["3.8"]

_DEFAULT_STORAGE_HOST = "https://storage.googleapis.com"


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session):
    """Run linters.

    Returns a failure if the linters find linting errors or sufficiently
    serious code quality issues.
    """
    session.install("flake8", BLACK_VERSION)
    session.run(
        "black", "--check", *BLACK_PATHS,
    )
    session.run("flake8", "google", "tests")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def blacken(session):
    """Run black.

    Format code to uniform standard.
    """
    session.install(BLACK_VERSION)
    session.run(
        "black", *BLACK_PATHS,
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint_setup_py(session):
    """Verify that setup.py is valid (including RST check)."""
    session.install("docutils", "pygments")
    session.run("python", "setup.py", "check", "--restructuredtext", "--strict")


def default(session):
    # Install all test dependencies, then install this package in-place.
    session.install("mock", "pytest", "pytest-cov")
    session.install("-e", ".")

    # Run py.test against the unit tests.
    session.run(
        "py.test",
        "--quiet",
        "--cov=google.cloud.storage",
        "--cov=google.cloud",
        "--cov=tests.unit",
        "--cov-append",
        "--cov-config=.coveragerc",
        "--cov-report=",
        "--cov-fail-under=0",
        os.path.join("tests", "unit"),
        *session.posargs,
    )


@nox.session(python=UNIT_TEST_PYTHON_VERSIONS)
def unit(session):
    """Run the unit test suite."""
    default(session)


@nox.session(python=SYSTEM_TEST_PYTHON_VERSIONS)
def system(session):
    """Run the system test suite."""
    system_test_path = os.path.join("tests", "system.py")
    system_test_folder_path = os.path.join("tests", "system")

    # Check the value of `RUN_SYSTEM_TESTS` env var. It defaults to true.
    if os.environ.get("RUN_SYSTEM_TESTS", "true") == "false":
        session.skip("RUN_SYSTEM_TESTS is set to false, skipping")
    # Environment check: Only run tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable")
    # mTLS tests requires pyopenssl.
    if os.environ.get("GOOGLE_API_USE_CLIENT_CERTIFICATE", "") == "true":
        session.install("pyopenssl")

    system_test_exists = os.path.exists(system_test_path)
    system_test_folder_exists = os.path.exists(system_test_folder_path)
    # Environment check: only run tests if found.
    if not system_test_exists and not system_test_folder_exists:
        session.skip("System tests were not found")

    # Use pre-release gRPC for system tests.
    session.install("--pre", "grpcio")

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    # 2021-05-06: defer installing 'google-cloud-*' to after this package,
    #             in order to work around Python 2.7 googolapis-common-protos
    #             issue.
    session.install(
        "mock", "pytest",
    )
    session.install("-e", ".")
    session.install(
        "google-cloud-testutils",
        "google-cloud-iam",
        "google-cloud-pubsub < 2.0.0",
        "google-cloud-kms < 2.0dev",
    )

    # Run py.test against the system tests.
    if system_test_exists:
        session.run("py.test", "--quiet", system_test_path, *session.posargs)
    if system_test_folder_exists:
        session.run("py.test", "--quiet", system_test_folder_path, *session.posargs)


@nox.session(python=CONFORMANCE_TEST_PYTHON_VERSIONS)
def conformance(session):
    """Run the conformance test suite."""
    conformance_test_path = os.path.join("tests", "conformance.py")
    conformance_test_folder_path = os.path.join("tests", "conformance")

    # Environment check: Only run tests if the STORAGE_EMULATOR_HOST is set.
    if (
        os.environ.get("STORAGE_EMULATOR_HOST", _DEFAULT_STORAGE_HOST)
        == _DEFAULT_STORAGE_HOST
    ):
        session.skip("Set STORAGE_EMULATOR_HOST to run, skipping")
    # Environment check: Only run tests if the environment variable is set.
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", ""):
        session.skip("Credentials must be set via environment variable")

    conformance_test_exists = os.path.exists(conformance_test_path)
    conformance_test_folder_exists = os.path.exists(conformance_test_folder_path)
    # Environment check: only run tests if found.
    if not conformance_test_exists and not conformance_test_folder_exists:
        session.skip("Conformance tests were not found")

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    # 2021-05-06: defer installing 'google-cloud-*' to after this package,
    #             in order to work around Python 2.7 googolapis-common-protos
    #             issue.
    session.install("pytest",)
    session.install("-e", ".")
    session.install(
        "google-cloud-testutils",
        "google-cloud-iam",
        "google-cloud-pubsub < 2.0.0",
        "google-cloud-kms < 2.0dev",
    )

    # Run py.test against the conformance tests.
    if conformance_test_exists:
        session.run("py.test", "--quiet", conformance_test_path, *session.posargs)
    if conformance_test_folder_exists:
        session.run(
            "py.test", "--quiet", conformance_test_folder_path, *session.posargs
        )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def cover(session):
    """Run the final coverage report.

    This outputs the coverage report aggregating coverage from the unit
    test runs (not system test runs), and then erases coverage data.
    """
    session.install("coverage", "pytest-cov")
    session.run("coverage", "report", "--show-missing", "--fail-under=100")

    session.run("coverage", "erase")


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docs(session):
    """Build the docs for this library."""

    session.install("-e", ".")
    session.install("sphinx", "alabaster", "recommonmark")

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-W",  # warnings as errors
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )


@nox.session(python=DEFAULT_PYTHON_VERSION)
def docfx(session):
    """Build the docfx yaml files for this library."""

    session.install("-e", ".")
    session.install("sphinx", "alabaster", "recommonmark", "gcp-sphinx-docfx-yaml")

    shutil.rmtree(os.path.join("docs", "_build"), ignore_errors=True)
    session.run(
        "sphinx-build",
        "-T",  # show full traceback on exception
        "-N",  # no colors
        "-D",
        (
            "extensions=sphinx.ext.autodoc,"
            "sphinx.ext.autosummary,"
            "docfx_yaml.extension,"
            "sphinx.ext.intersphinx,"
            "sphinx.ext.coverage,"
            "sphinx.ext.napoleon,"
            "sphinx.ext.todo,"
            "sphinx.ext.viewcode,"
            "recommonmark"
        ),
        "-b",
        "html",
        "-d",
        os.path.join("docs", "_build", "doctrees", ""),
        os.path.join("docs", ""),
        os.path.join("docs", "_build", "html", ""),
    )
