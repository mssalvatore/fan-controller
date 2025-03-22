# Fan Controller

A simple fan controller for one PC case fan.


## BOM

### 3D-printed parts

| Name | Quantity |
| --- | --- |
| [Box](./renders/box.stl) | 1 |
| [Lid](./renders/lid.stl) | 1 |

### Off-the-shelf parts
| Name | Quantity |
| --- | --- |
| 5.5m DC female connector | 1 |
| 12v DC power supply | 1 |
| M4-.70 x 10 screw | 2 |
| M4-compatible washer | 2 |
| M4 nut | 2 |
| PG-7 cable gland | 1 |
| ZFC4-1KM PWM fan controller | 1 |


## Rendering an STL

Follow these steps to render an STL:

```shell
$ pip install poetry
$ poetry install
$ poetry run python -m fan_controller/fan_controller.py --stl
```

The rendered file will be saved to `renders/fan_controller.stl`.
