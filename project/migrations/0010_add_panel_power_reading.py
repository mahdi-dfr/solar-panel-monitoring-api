# Generated manually for PanelPowerReading

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0009_remove_panel_volatge_panel_kw"),
    ]

    operations = [
        migrations.CreateModel(
            name="PanelPowerReading",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kw", models.DecimalField(decimal_places=4, max_digits=12, verbose_name="توان")),
                ("recorded_at", models.DateTimeField(db_index=True, verbose_name="زمان ثبت")),
                (
                    "panel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="power_readings",
                        to="project.panel",
                        verbose_name="پنل",
                    ),
                ),
            ],
            options={
                "verbose_name": "قرائت توان پنل",
                "verbose_name_plural": "قرائت‌های توان پنل",
                "ordering": ["-recorded_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="panelpowerreading",
            constraint=models.UniqueConstraint(fields=("panel", "recorded_at"), name="unique_panel_recorded_at"),
        ),
    ]
