# Generated by Django 2.2.7 on 2021-05-20 05:33

import CV_APP.validators
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aspectos_generales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Años',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Colegios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('imagen', models.ImageField(blank=True, default=False, null=True, unique=True, upload_to='colegios_images', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Colegios2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('imagen', models.ImageField(blank=True, default=False, null=True, unique=True, upload_to='colegios_images', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Colegios3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('imagen', models.ImageField(blank=True, default=False, null=True, unique=True, upload_to='colegios_images', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Competencias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Conclusion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Criterios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Disposicion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Ingles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Nivel_ingles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Nivel_Tec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='opcion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Postulacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('apellido_p', models.CharField(max_length=250, verbose_name='Apellido Paterno')),
                ('apellido_m', models.CharField(max_length=250, verbose_name='Apellido Materno')),
                ('rut', models.CharField(max_length=250, validators=[django.core.validators.MinLengthValidator(8)])),
                ('telefono', models.CharField(help_text='El formato debe ser el siguiente +569xxxxxxxx', max_length=250, verbose_name='Teléfono')),
                ('email', models.EmailField(max_length=254, verbose_name='Correo')),
                ('cv', models.FileField(help_text='Solo se permiten archivos PDF', upload_to='cv', validators=[CV_APP.validators.validate_file_extension], verbose_name='Adjuntar CV')),
                ('otros_documentos', models.FileField(blank=True, help_text='Solo se permiten archivos PDF', null=True, upload_to='cv', validators=[CV_APP.validators.validate_file_extension], verbose_name='Otros Documentos')),
                ('ficha_fat', models.FileField(blank=True, null=True, upload_to='FAT', verbose_name='Adjuntar Ficha FAT')),
                ('carta_oferta', models.FileField(blank=True, null=True, upload_to='CARTA_OFERTA', verbose_name='Adjuntar carta oferta')),
                ('valido', models.BooleanField(default=False, verbose_name='Aprobar')),
                ('email_send', models.BooleanField(default=False, verbose_name='Email_enviado')),
                ('send', models.BooleanField(default=False, verbose_name='Email_enviado_monica')),
                ('rechazar', models.BooleanField(default=False, verbose_name='Rechazar psicolaboral')),
                ('rechazar_rector', models.BooleanField(default=False, verbose_name='Rechazar')),
                ('rechazar_coordinador', models.BooleanField(default=False, verbose_name='Rechazar Coordinador')),
                ('aceptada', models.BooleanField(default=False, verbose_name='Aceptada')),
                ('rechazada', models.BooleanField(default=False, verbose_name='Rechazada')),
                ('Siguiente', models.BooleanField(default=False, verbose_name='Entrevistar')),
                ('liberar', models.BooleanField(default=False, verbose_name='Liberar para todos')),
                ('aprobar_demos', models.BooleanField(default=False, verbose_name='Aprobar')),
                ('rechazar_demos', models.BooleanField(default=False, verbose_name='No aprobar')),
                ('entrevistado', models.BooleanField(default=False, verbose_name='Entrevistado')),
                ('entrevistado_demo', models.BooleanField(default=False, verbose_name='Entrevistado_demo')),
                ('psicologa', models.BooleanField(default=False, verbose_name='Aprobar psicolaboral')),
                ('psicologa1', models.BooleanField(default=False, verbose_name='a Daisy Lasen')),
                ('psicologa2', models.BooleanField(default=False, verbose_name='a María Francisca Molina')),
                ('enviada', models.DateField(auto_now_add=True)),
                ('nombre_r', models.CharField(max_length=250, verbose_name='Nombre')),
                ('cargo_r', models.CharField(max_length=250, verbose_name='Cargo')),
                ('corre_r', models.EmailField(max_length=254, verbose_name='Correo')),
                ('telefono_r', models.CharField(help_text='El formato debe ser el siguiente +569xxxxxxxx', max_length=250, verbose_name='Teléfono')),
                ('relacion_r', models.CharField(max_length=250, verbose_name='Relación laboral')),
                ('instituto_r', models.CharField(max_length=250, verbose_name='Institución')),
                ('nombre_r_2', models.CharField(max_length=250, verbose_name='Nombre')),
                ('cargo_r_2', models.CharField(max_length=250, verbose_name='Cargo')),
                ('corre_r_2', models.EmailField(max_length=254, verbose_name='Correo')),
                ('telefono_r_2', models.CharField(help_text='El formato debe ser el siguiente +569xxxxxxxx', max_length=250, verbose_name='Teléfono')),
                ('relacion_r_2', models.CharField(max_length=250, verbose_name='Relación laboral')),
                ('instituto_r_2', models.CharField(max_length=250, verbose_name='Institución')),
                ('liberar_2', models.BooleanField(default=False, verbose_name='Liberar preferencia 2')),
                ('liberar_3', models.BooleanField(default=False, verbose_name='Liberar preferencia 3')),
                ('coordinador', models.BooleanField(default=False, verbose_name='coordinador')),
                ('rechazar_index', models.BooleanField(default=False, verbose_name='Rechazar')),
                ('liberar_coordinador', models.BooleanField(default=False, verbose_name='Liberar')),
                ('liberar_equipomulti', models.BooleanField(default=False, verbose_name='Liberar')),
                ('fecha_fat', models.DateField(auto_now_add=True)),
                ('fecha_oferta', models.DateField(auto_now_add=True)),
                ('carta_oferta_recibida', models.BooleanField(default=False, verbose_name='carta oferta recibida')),
                ('finalizado', models.BooleanField(verbose_name='Finalizar')),
                ('coordinador_entrevisto', models.CharField(blank=True, max_length=250, null=True, verbose_name='Coordinador/a FFEBE que entrevistó')),
                ('observaciones_c', models.TextField(blank=True, max_length=250, null=True, verbose_name='Observaciones Coordinador/a FEBE')),
                ('aceptar_ficha', models.BooleanField(default=False, verbose_name='Aceptar ficha F.A.T')),
                ('años', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CV_APP.Años', verbose_name='Años de experiencia')),
                ('cargo', models.ForeignKey(help_text='Cargo al que postula', on_delete=django.db.models.deletion.CASCADE, to='CV_APP.Cargo')),
                ('colegio1', models.ForeignKey(help_text='Colegio al que postula', on_delete=django.db.models.deletion.CASCADE, related_name='colegio1', to='CV_APP.Colegios', verbose_name='Preferencia 1')),
                ('colegio2', models.ForeignKey(blank=True, help_text='Colegio al que postula', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colegio2', to='CV_APP.Colegios', verbose_name='Preferencia 2')),
                ('colegio3', models.ForeignKey(blank=True, help_text='Colegio al que postula', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colegio3', to='CV_APP.Colegios', verbose_name='Preferencia 3')),
                ('disponibilidad', models.ManyToManyField(help_text='Puede escoger más de una.', related_name='disponibilidad', to='CV_APP.Disposicion')),
                ('nivel_ingles', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CV_APP.Nivel_ingles', verbose_name='Nivel Inglés')),
                ('nivel_tec', models.ManyToManyField(help_text='Puede escoger más de una.', to='CV_APP.Nivel_Tec', verbose_name='Dominio de herramientas tecnológicas')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_administrador', models.BooleanField(default=False)),
                ('is_coordinacion', models.BooleanField(default=False)),
                ('is_coordinacion2', models.BooleanField(default=False)),
                ('is_rector', models.BooleanField(default=False)),
                ('is_psicologa', models.BooleanField(default=False)),
                ('is_monica', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Titulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('cargo', models.ManyToManyField(blank=True, null=True, related_name='Titulo_cargo', to='CV_APP.Cargo', verbose_name='cargo')),
            ],
        ),
        migrations.CreateModel(
            name='Rubrica_psicologa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fortalezas', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('fortalezas2', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('fortalezas3', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('posibilidades', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('posibilidades2', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('posibilidades3', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('sugerencias', models.TextField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('realizada', models.DateField(auto_now_add=True)),
                ('aspecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aspectos_1', to='CV_APP.Aspectos_generales', verbose_name='')),
                ('aspecto_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CV_APP.Aspectos_generales', verbose_name='')),
                ('competencia_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_1', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_10', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_10', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_11', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_11', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_12', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_12', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_13', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_13', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_14', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_14', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_15', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_15', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_16', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_16', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_17', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_17', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_18', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_18', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_19', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_19', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_2', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_3', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_4', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_5', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_6', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_7', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_7', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_8', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_8', to='CV_APP.Competencias', verbose_name='')),
                ('competencia_9', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competencia_9', to='CV_APP.Competencias', verbose_name='')),
                ('conclusion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CV_APP.Conclusion', verbose_name='')),
                ('postulantes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulantes', to='CV_APP.Postulacion')),
            ],
        ),
        migrations.CreateModel(
            name='Rubrica_equipomulti',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrevistado', models.BooleanField(default=True, verbose_name='Entrevistado')),
                ('puntos', models.IntegerField()),
                ('puntos2', models.IntegerField(verbose_name='Puntos')),
                ('puntos3', models.IntegerField(verbose_name='Puntos')),
                ('puntos4', models.IntegerField(verbose_name='Puntos')),
                ('puntos5', models.IntegerField(verbose_name='Puntos')),
                ('puntos6', models.IntegerField(verbose_name='Puntos')),
                ('puntos7', models.IntegerField(verbose_name='Puntos')),
                ('puntos8', models.IntegerField(verbose_name='Puntos')),
                ('puntos9', models.IntegerField(verbose_name='Puntos')),
                ('comentario', models.TextField(max_length=1000)),
                ('comentario2', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario3', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario4', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario5', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario6', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario7', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario8', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario9', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('rechazar', models.BooleanField(default=False, verbose_name='rechazado')),
                ('observaciones', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('liberar', models.BooleanField(default=False, verbose_name='liberar')),
                ('cargop', models.CharField(max_length=1000, verbose_name='')),
                ('niveles', models.CharField(max_length=1000, verbose_name='')),
                ('Nombre_referencia_y_cargo_actual', models.CharField(max_length=1000, verbose_name='')),
                ('Relación_laboral_con_postulante', models.CharField(max_length=1000, verbose_name='')),
                ('cometarios_referencias', models.TextField(help_text='fortalezas, áreas de mejora, asunto por qué dejó su trabajo', max_length=1000, verbose_name='')),
                ('renumeracion', models.CharField(max_length=250, verbose_name='')),
                ('horas', models.CharField(max_length=15, verbose_name='')),
                ('realizada', models.DateField(auto_now_add=True)),
                ('opcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CV_APP.opcion', verbose_name='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Owner_postulacion_em', to=settings.AUTH_USER_MODEL)),
                ('postulacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulacion_em', to='CV_APP.Postulacion')),
            ],
        ),
        migrations.CreateModel(
            name='Rubrica_demo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observaciones', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('realizada', models.DateField(auto_now_add=True)),
                ('criterio_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_1', to='CV_APP.Criterios')),
                ('criterio_10', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_10', to='CV_APP.Criterios')),
                ('criterio_11', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_11', to='CV_APP.Criterios')),
                ('criterio_12', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_12', to='CV_APP.Criterios')),
                ('criterio_13', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_13', to='CV_APP.Criterios')),
                ('criterio_14', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_14', to='CV_APP.Criterios')),
                ('criterio_15', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_15', to='CV_APP.Criterios')),
                ('criterio_16', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_16', to='CV_APP.Criterios')),
                ('criterio_17', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_17', to='CV_APP.Criterios')),
                ('criterio_18', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_18', to='CV_APP.Criterios')),
                ('criterio_19', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_19', to='CV_APP.Criterios')),
                ('criterio_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_2', to='CV_APP.Criterios')),
                ('criterio_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_3', to='CV_APP.Criterios')),
                ('criterio_4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_4', to='CV_APP.Criterios')),
                ('criterio_5', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_5', to='CV_APP.Criterios')),
                ('criterio_6', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_6', to='CV_APP.Criterios')),
                ('criterio_7', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_7', to='CV_APP.Criterios')),
                ('criterio_8', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_8', to='CV_APP.Criterios')),
                ('criterio_9', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criterio_9', to='CV_APP.Criterios')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Owner_postulacion_demo', to=settings.AUTH_USER_MODEL)),
                ('postulacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulacion_demo', to='CV_APP.Postulacion')),
            ],
        ),
        migrations.CreateModel(
            name='Rubrica_coordinador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrevistado', models.BooleanField(default=True, verbose_name='Entrevistado_c')),
                ('puntos', models.IntegerField()),
                ('puntos2', models.IntegerField(verbose_name='Puntos')),
                ('puntos3', models.IntegerField(verbose_name='Puntos')),
                ('puntos4', models.IntegerField(verbose_name='Puntos')),
                ('puntos5', models.IntegerField(verbose_name='Puntos')),
                ('puntos6', models.IntegerField(verbose_name='Puntos')),
                ('puntos7', models.IntegerField(verbose_name='Puntos')),
                ('comentario', models.TextField(max_length=1000)),
                ('comentario2', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario3', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario4', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario5', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario6', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario7', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('rechazar', models.BooleanField(default=False, verbose_name='rechazado')),
                ('observaciones', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('liberar', models.BooleanField(default=False, verbose_name='liberar')),
                ('cargop', models.CharField(max_length=1000, verbose_name='')),
                ('niveles', models.CharField(max_length=1000, verbose_name='')),
                ('Nombre_referencia_y_cargo_actual', models.CharField(max_length=1000, verbose_name='')),
                ('Relación_laboral_con_postulante', models.CharField(max_length=1000, verbose_name='')),
                ('cometarios_referencias', models.TextField(help_text='fortalezas, áreas de mejora, asunto por qué dejó su trabajo', max_length=1000, verbose_name='')),
                ('renumeracion', models.CharField(max_length=250, verbose_name='')),
                ('horas', models.CharField(max_length=15, verbose_name='')),
                ('realizada', models.DateField(auto_now_add=True)),
                ('opcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CV_APP.opcion', verbose_name='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Owner_postulacion_c', to=settings.AUTH_USER_MODEL)),
                ('postulacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulacion_c', to='CV_APP.Postulacion')),
            ],
        ),
        migrations.CreateModel(
            name='Rubrica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrevistado', models.BooleanField(default=True, verbose_name='Entrevistado')),
                ('puntos', models.IntegerField()),
                ('puntos2', models.IntegerField(verbose_name='Puntos')),
                ('puntos3', models.IntegerField(verbose_name='Puntos')),
                ('puntos4', models.IntegerField(verbose_name='Puntos')),
                ('puntos5', models.IntegerField(verbose_name='Puntos')),
                ('puntos6', models.IntegerField(verbose_name='Puntos')),
                ('puntos7', models.IntegerField(verbose_name='Puntos')),
                ('puntos8', models.IntegerField(verbose_name='Puntos')),
                ('puntos9', models.IntegerField(verbose_name='Puntos')),
                ('puntos10', models.IntegerField(verbose_name='Puntos')),
                ('comentario', models.TextField(max_length=1000)),
                ('comentario2', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario3', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario4', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario5', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario6', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario7', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario8', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario9', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('comentario10', models.TextField(max_length=1000, verbose_name='Comentario')),
                ('observaciones', models.CharField(blank=True, max_length=1000, null=True, verbose_name='')),
                ('cargop', models.CharField(max_length=1000, verbose_name='')),
                ('niveles', models.CharField(max_length=1000, verbose_name='')),
                ('Nombre_referencia_y_cargo_actual', models.CharField(max_length=1000, verbose_name='')),
                ('Relación_laboral_con_postulante', models.CharField(max_length=1000, verbose_name='')),
                ('cometarios_referencias', models.TextField(help_text='fortalezas, áreas de mejora, asunto por qué dejó su trabajo', max_length=1000, verbose_name='')),
                ('renumeracion', models.CharField(max_length=250, verbose_name='')),
                ('horas', models.CharField(max_length=15, verbose_name='')),
                ('realizada', models.DateField(auto_now_add=True)),
                ('opcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CV_APP.opcion', verbose_name='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Owner_postulacion', to=settings.AUTH_USER_MODEL)),
                ('postulacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulacion', to='CV_APP.Postulacion')),
            ],
        ),
        migrations.AddField(
            model_name='postulacion',
            name='rector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rector_cargo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postulacion',
            name='titulo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CV_APP.Titulo', verbose_name='Título'),
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CV_APP.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Rector',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('colegio', models.ManyToManyField(blank=True, related_name='colegio_rector', to='CV_APP.Colegios')),
            ],
        ),
        migrations.CreateModel(
            name='Psicologa',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('psicologa1', models.BooleanField(default=False, verbose_name='Psicologa1')),
                ('psicologa2', models.BooleanField(default=False, verbose_name='Psicologa2')),
                ('colegio', models.ManyToManyField(blank=True, related_name='colegio_psicologa', to='CV_APP.Colegios')),
            ],
        ),
        migrations.CreateModel(
            name='Monica',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('colegio', models.ManyToManyField(blank=True, related_name='colegio_monica', to='CV_APP.Colegios')),
            ],
        ),
        migrations.CreateModel(
            name='Coordinacion2',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('colegio', models.ManyToManyField(blank=True, related_name='colegio_coordinacion2', to='CV_APP.Colegios')),
            ],
        ),
        migrations.CreateModel(
            name='Coordinacion',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('colegio', models.ManyToManyField(blank=True, related_name='colegio_coordinacion', to='CV_APP.Colegios')),
            ],
        ),
    ]
