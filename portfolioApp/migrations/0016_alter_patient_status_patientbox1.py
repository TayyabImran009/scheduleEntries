# Generated by Django 4.0.1 on 2022-04-07 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioApp', '0015_alter_patient_aligners_alter_patient_archform_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='Status',
            field=models.CharField(choices=[('Accept', 'Accept'), ('Review', 'Review'), ('Decline', 'Decline'), ('On-Hold', 'On-Hold'), ('New', 'New')], default='Pending', max_length=120, null=True),
        ),
        migrations.CreateModel(
            name='PatientBox1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage1', models.BooleanField(default=False)),
                ('stage2', models.BooleanField(default=False)),
                ('stage3', models.BooleanField(default=False)),
                ('stage4', models.BooleanField(default=False)),
                ('stage5', models.BooleanField(default=False)),
                ('stage6', models.BooleanField(default=False)),
                ('stage7', models.BooleanField(default=False)),
                ('stage8', models.BooleanField(default=False)),
                ('stage9', models.BooleanField(default=False)),
                ('stage10', models.BooleanField(default=False)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='portfolioApp.patient')),
            ],
        ),
    ]
