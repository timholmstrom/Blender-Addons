# MSwap
Blender add-on for swapping materials with fake-user materials.

# WIP

# How to install:
1. Download the .zip file containing the addon.

2. In the addons tab in Blenders user preferences, press "install from file".

3. Chose the .zip file containing this addon.

4. Activate the addon.


# How to use the addon:
# When I write "Viewport Color" I mean the "Diffuse Color"!

Assuming you already have some fake-user materials in your scene, change the Viewport Color of your fake-user material to the same color as the material's Viewport Color you want it to swap with.


# Example:
You have 1 cube with a material in your Blender scene that you want to swap for another pre-made fake-user material.

The button "Swap Materials" will check if the selected objects Viewport Color matches (or is close to) any fake-user's Viewport Color in the scene. If it is, it will change the material of that object to the fake-user material with the closest matching Viewport Color.


Let's say your cube has a Viewport Color of (0.15, 0.15, 0.15) and you have a material(fake-user) named "Metal_Dark" in the scene with a Viewport Color of (0.1, 0.1, 0.1).
Assuming no other fake-user material has it's Viewport Color closer to the cube, your cube-material will be swapped with "Metal_Dark".

# Note:
In the panel, "Color Threshold" dictates how close the colors values have to be in order to be a match. If the closest match is above 0.08(standard settings) it will add a placeholder material instead. So I urge you to have a fake-user material in your scene named "PlaceholderMaterial". That way you will see if something went wrong when the script changed the materials.
