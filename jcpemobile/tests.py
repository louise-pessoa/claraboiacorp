from django.test import TestCase, Client
from django.utils import timezone
import datetime
from django.core.management import call_command

from jcpemobile.models import Noticia, Visualizacao, NoticiaRankingDaily


class VisualizacaoAndRankingTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.noticia = Noticia.objects.create(slug='t-noticia', titulo='T', conteudo='x')

	def test_visualizacao_por_ip_por_dia(self):
		# mesmo IP no mesmo dia não gera visualização duplicada
		resp1 = self.client.get(f'/noticias/{self.noticia.slug}/?fake_ip=1.2.3.4')
		resp2 = self.client.get(f'/noticias/{self.noticia.slug}/?fake_ip=1.2.3.4')
		self.assertEqual(200, resp1.status_code)
		self.assertEqual(200, resp2.status_code)
		self.assertEqual(1, Visualizacao.objects.filter(noticia=self.noticia, ip_usuario='1.2.3.4').count())

	def test_update_daily_ranking_sets_ranking(self):
		# cria visualizacoes ontem para 2 noticias com diferentes IPs
		other = Noticia.objects.create(slug='t-noticia-2', titulo='T2', conteudo='y')
		yesterday = (timezone.now() - datetime.timedelta(days=1)).date()
		dt = timezone.make_aware(datetime.datetime.combine(yesterday, datetime.time(hour=12)))

		# 3 views para noticia1
		for i in range(3):
			Visualizacao.objects.create(noticia=self.noticia, ip_usuario=f'10.0.0.{i}', data=dt)
		# 1 view para noticia2
		Visualizacao.objects.create(noticia=other, ip_usuario='10.0.1.1', data=dt)

		# rodar comando
		call_command('update_daily_ranking')

		# verificar NoticiaRankingDaily
		r1 = NoticiaRankingDaily.objects.filter(noticia=self.noticia, date=yesterday).first()
		r2 = NoticiaRankingDaily.objects.filter(noticia=other, date=yesterday).first()
		self.assertIsNotNone(r1)
		self.assertEqual(3, r1.views)
		self.assertIsNotNone(r2)
		self.assertEqual(1, r2.views)

		# verificar daily_rank (noticia com mais views deve ter rank 1)
		n1 = Noticia.objects.get(id=self.noticia.id)
		n2 = Noticia.objects.get(id=other.id)
		self.assertEqual(1, n1.daily_rank)
		self.assertEqual(yesterday, n1.daily_rank_date)
