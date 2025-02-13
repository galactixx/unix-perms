# unix-perms
![Tests](https://github.com/galactixx/unix-perms/actions/workflows/continuous_integration.yaml/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/unix-perms.svg)](https://pypi.org/project/unix-perms/)
[![Python versions](https://img.shields.io/pypi/pyversions/unix-perms.svg)](https://pypi.org/project/unix-perms/)
[![License](https://img.shields.io/github/license/galactixx/unix-perms.svg)](https://github.com/galactixx/unix-perms/blob/main/LICENSE)
![PyPI Downloads](https://static.pepy.tech/badge/unix-perms/month)
![PyPI Downloads](https://static.pepy.tech/badge/unix-perms)

Manage and interpret Unix file permissions with a Python package that provides intuitive tools for creating, validating, and describing permission modes.

## 📦 **Installation**

To install unix-perms, run the following command:

```bash
pip install unix-perms
```

## 🚀 **Features**
- Convert octal digits to permission configurations.
- Convert octal representations to Unix permission modes.
- Validate Unix permission modes.
- Create, update, and work with permissions modes using python objects.

## 📚 **Usage**

### Convert an Octal Digit to Configuration
```python
from unix_perms import from_octal_digit_to_config

config = from_octal_digit_to_config(7)
print(config)
```

```python
OctalConfig(
    description='Read, write, and execute permissions',
    read=True,
    write=True,
    execute=True
)
```

### Convert Octal Representation to Unix Permissions Mode
```python
from unix_perms import from_octal_to_permissions_mode

mode = from_octal_to_permissions_mode(0o777)
print(mode)
```

```python
777
```

### Validate if an Octal Representation is a Unix Permissions Mode
```python
from unix_perms import is_permissions_mode

print(is_permissions_mode('755'))
print(is_permissions_mode('999'))
```

```python
True
False
```

### Using `PermissionsConfig`
```python
from unix_perms import PermissionsConfig

config = PermissionsConfig.from_octal_digit(4)
print(config)
```

```python
PermissionsConfig(read=True, write=False, execute=False)
```

### Using `PermissionsByte`
```python
from unix_perms import PermissionsByte, PermissionsConfig

config = PermissionsConfig(read=True, write=False, execute=False)
owner_permissions = PermissionsByte(authority="owner", config=config)

print(owner_permissions.permissions_mode)
print(owner_permissions.permissions_description)
```

```python
400
Read permission only
```

### Using `PermissionsMode`
```python
from unix_perms import PermissionsByte, PermissionsConfig, PermissionsMode

owner_permissions = PermissionsByte(
    authority="owner", config=WRITE_PERMISSIONS_CONFIG
)
group_permissions = PermissionsByte(
    authority="group", config=ALL_PERMISSIONS_CONFIG
)
others_permissions = PermissionsByte(
    authority="others", config=READ_PERMISSIONS_CONFIG
)

permissions_mode = PermissionsMode(
    owner=owner_permissions, group=group_permissions, others=others_permissions
)
print(permissions_mode.permissions_mode)

group_permissions_new = PermissionsByte(
    authority="group", config=ALL_PERMISSIONS_CONFIG
)
permission_mode_sub = permissions_mode - group_permissions_new
print(permission_mode_sub.permissions_mode)
```

```python
274
204
```

## 🤝 **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 📞 **Contact**

If you have any questions or need support, feel free to reach out by opening an issue on the [GitHub repository](#).
