# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-18 11:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_individual_phenotips_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('loaded_date', models.DateTimeField(blank=True, null=True)),
                ('sequencing_type', models.CharField(choices=[(b'WES', b'Exome'), (b'WGS', b'Whole Genome')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='VariantCallsetSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mean_target_coverage', models.FloatField(blank=True, null=True)),
                ('coverage_status', models.CharField(choices=[(b'S', b'In Sequencing'), (b'I', b'Interim'), (b'C', b'Complete'), (b'A', b'Abandoned')], default=b'S', max_length=1)),
                ('bam_file_path', models.CharField(blank=True, default=b'', max_length=1000)),
                ('HET_HOMVAR_RATIO', models.FloatField(blank=True, null=True)),
                ('TOTAL_SNPS', models.IntegerField(blank=True, null=True)),
                ('NUM_IN_DB_SNP', models.IntegerField(blank=True, null=True)),
                ('NOVEL_SNPS', models.IntegerField(blank=True, null=True)),
                ('FILTERED_SNPS', models.IntegerField(blank=True, null=True)),
                ('PCT_DBSNP', models.FloatField(blank=True, null=True)),
                ('DBSNP_TITV', models.FloatField(blank=True, null=True)),
                ('NOVEL_TITV', models.FloatField(blank=True, null=True)),
                ('TOTAL_INDELS', models.IntegerField(blank=True, null=True)),
                ('NOVEL_INDELS', models.IntegerField(blank=True, null=True)),
                ('FILTERED_INDELS', models.IntegerField(blank=True, null=True)),
                ('PCT_DBSNP_INDELS', models.FloatField(blank=True, null=True)),
                ('NUM_IN_DB_SNP_INDELS', models.IntegerField(blank=True, null=True)),
                ('DBSNP_INS_DEL_RATIO', models.FloatField(blank=True, null=True)),
                ('NOVEL_INS_DEL_RATIO', models.FloatField(blank=True, null=True)),
                ('TOTAL_MULTIALLELIC_SNPS', models.IntegerField(blank=True, null=True)),
                ('NUM_IN_DB_SNP_MULTIALLELIC', models.IntegerField(blank=True, null=True)),
                ('TOTAL_COMPLEX_INDELS', models.IntegerField(blank=True, null=True)),
                ('NUM_IN_DB_SNP_COMPLEX_INDELS', models.IntegerField(blank=True, null=True)),
                ('SNP_REFERENCE_BIAS', models.FloatField(blank=True, null=True)),
                ('NUM_SINGLETONS', models.IntegerField(blank=True, null=True)),
                ('PCT_CHIMERAS', models.FloatField(blank=True, null=True)),
                ('FREEMIX', models.FloatField(blank=True, null=True)),
                ('GQ0_FRACTION', models.FloatField(blank=True, null=True)),
                ('PCT_TARGET_BASES_20X', models.FloatField(blank=True, null=True)),
                ('AT_DROPOUT', models.FloatField(blank=True, null=True)),
                ('GC_DROPOUT', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='individualphenotype',
            name='individual',
        ),
        migrations.RemoveField(
            model_name='individualphenotype',
            name='phenotype',
        ),
        migrations.RemoveField(
            model_name='projectphenotype',
            name='project',
        ),
        migrations.RenameField(
            model_name='individual',
            old_name='gender',
            new_name='sex',
        ),
        migrations.RemoveField(
            model_name='family',
            name='after_load_qc_json',
        ),
        migrations.RemoveField(
            model_name='family',
            name='before_load_qc_json',
        ),
        migrations.RemoveField(
            model_name='family',
            name='has_after_load_qc_error',
        ),
        migrations.RemoveField(
            model_name='family',
            name='has_before_load_qc_error',
        ),
        migrations.RemoveField(
            model_name='family',
            name='relatedness_matrix_json',
        ),
        migrations.RemoveField(
            model_name='family',
            name='variant_stats_json',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='coverage_file',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='exome_depth_file',
        ),
        migrations.RemoveField(
            model_name='vcffile',
            name='needs_reannotate',
        ),
        migrations.AddField(
            model_name='project',
            name='supports_versions',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='VariantCallset',
            fields=[
                ('dataset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='base.Dataset')),
                ('dataset_id', models.SlugField(blank=True, default=b'', max_length=140)),
                ('mongo_gene_search_coll', models.CharField(blank=True, max_length=100, null=True)),
            ],
            bases=('base.dataset',),
        ),
        migrations.DeleteModel(
            name='IndividualPhenotype',
        ),
        migrations.DeleteModel(
            name='ProjectPhenotype',
        ),
        migrations.AddField(
            model_name='variantcallsetsample',
            name='individual',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Individual'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='vcf_files',
            field=models.ManyToManyField(blank=True, to='base.VCFFile'),
        ),
        migrations.AddField(
            model_name='variantcallsetsample',
            name='variant_callset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.VariantCallset'),
        ),
        migrations.AddField(
            model_name='variantcallset',
            name='individuals',
            field=models.ManyToManyField(through='base.VariantCallsetSample', to='base.Individual'),
        ),
    ]