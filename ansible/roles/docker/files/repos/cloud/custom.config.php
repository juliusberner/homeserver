<?php

$CONFIG = [

/**
 * Enforce token authentication for clients, which blocks requests using the user
 * password for enhanced security. Users need to generate tokens in personal settings
 * which can be used as passwords on their clients.
 *
 * Defaults to ``false``
 */
'token_auth_enforced' => true,

/**
 * By default WebAuthn is available but it can be explicitly disabled by admins
 */
'auth.webauthn.enabled' => false,

/**
 * The directory where the skeleton files are located. These files will be
 * copied to the data directory of new users. Leave empty to not copy any
 * skeleton files.
 * ``{lang}`` can be used as a placeholder for the language of the user.
 * If the directory does not exist, it falls back to non dialect (from ``de_DE``
 * to ``de``). If that does not exist either, it falls back to ``default``
 *
 * Defaults to ``core/skeleton`` in the Nextcloud directory.
 */
'skeletondirectory' => '',

/**
 * The directory where the template files are located. These files will be
 * copied to the template directory of new users. Leave empty to not copy any
 * template files.
 * ``{lang}`` can be used as a placeholder for the language of the user.
 * If the directory does not exist, it falls back to non dialect (from ``de_DE``
 * to ``de``). If that does not exist either, it falls back to ``default``
 *
 * If this is not set creating a template directory will only happen if no custom
 * ``skeletondirectory`` is defined, otherwise the shipped templates will be used
 * to create a template directory for the user.
 */
'templatedirectory' => '',

];