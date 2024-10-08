"""Tests for custom form validators."""
# pylint: disable=import-error
import pytest
from wtforms import ValidationError
from app.forms import verify_email_in_use, check_credentials, verify_username_in_use

def test_verify_email_in_use(mocker, form, session):
    """Confirms that verify_email_in_use function properly"""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Mock password_hash function
    mocker.patch("app.models.password_hash", return_value=form.password.data)
    #Check if test user exists
    with pytest.raises(ValidationError):
        verify_email_in_use(form, form.email)

def test_check_credentials(mocker, form, session):
    """Confirms that check_credentials function properly"""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Mock password_hash function
    mocker.patch("app.models.password_hash", return_value=form.password.data + "1")
    #Check if test user exists
    with pytest.raises(ValidationError):
        check_credentials(form, form.email)

def test_verify_username_in_use(mocker, form, session):
    """Confirms that verify_username_in_use function properly"""
    #Mock get_session function
    mocker.patch("app.models.get_session", return_value=session)
    #Mock password_hash function
    mocker.patch("app.models.password_hash", return_value=form.password.data)
    #Check if test user exists
    with pytest.raises(ValidationError):
        verify_username_in_use(form, form.username)
