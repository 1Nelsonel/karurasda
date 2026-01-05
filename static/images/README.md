# Static Images for Karura SDA Admin

## Required Images

Please add the following images to this directory:

1. **logo.png** - Church logo (recommended size: 150x150px)
   - Used in the admin sidebar and header
   - Should be a transparent PNG with the church logo

2. **church-background.jpg** - Login page background image (recommended size: 1920x1080px)
   - Used as the background image on the admin login page
   - Should be a high-quality image of the church or related imagery

## Where to Place Your Images

- Copy your logo file as: `logo.png`
- Copy your background image as: `church-background.jpg`

Both files should be placed in this `/static/images/` directory.

## After Adding Images

After adding the images, run:
```bash
python manage.py collectstatic
```

This will copy the images to the assets directory for production use.
