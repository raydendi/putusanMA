import scrapy

class PutusanSpider(scrapy.Spider):
    name = 'putusan'
    allowed_domains = ['putusan3.mahkamahagung.go.id']
    start_urls = ['https://putusan3.mahkamahagung.go.id/direktori/index/kategori/pidana-umum-1.html']

    # parsing
    def parse(self, response):
        for link in response.css('div.tab-container').xpath('//div[starts-with(@id,"tabs-1")]').xpath('//div[starts-with(@id,"popular-post-list-sidebar")]').css('div.spost.clearfix').css('div.entry-c').css('strong ::attr(href)'):
            yield response.follow(link.get(), callback=self.itemsInLink)
        next_url = response.css('div.pagging.text-center').css('nav').css('li.page-item')[-2].css('a.page-link ::attr(href)')
        #next_url_2 = response.css('div.pagging.text-center').css('nav').css('li.page-item')[6].css('a.page-link ::attr(href)')
        #for url in next_url:
        #    if  url== next_url[-2]:
        #        yield response.follow(url.css('a.page.link ::attr(href)').get(), callback=self.parse)
       # if next_url is not next_url:
        yield response.follow(next_url.get(), callback=self.parse)
       # else:
       #     yield response.follow(next_url_2.get(), callback=self.parse)
 
    #get item in link detail
    def itemsInLink(self, response):
        tabRight = response.css('div.col-sm-4.nobottommargin.col_last').css('div.card.bg-success.mb-3').xpath('//div[starts-with(@id,"headingThree")]').xpath('//div[starts-with(@id, "collapseThree")]').css('div.card-body.bg-white').xpath('//div[contains(@style,"margin-bottom: 10px")]').css('ul.portfolio-meta.nobottommargin')
        for item in response.css('table').css('tbody'):
            yield {
                  'Putusan': item.css('h2').getall(),
                  'Nomor Putusan': item.css('tr')[1].xpath('.//td/text()')[1].get().strip(),
                  'Tingkat Proses': item.css('tr')[2].xpath('.//td/text()')[1].get().strip(),
                  'Klasifikasi': item.css('tr')[3].xpath('.//td')[1].xpath('.//a/text()').getall(),
                  'Kata Kunci': item.css('tr')[4].xpath('.//td/text()')[1].get().strip(),
                  'Tahun': item.css('tr')[5].xpath('.//td/text()')[1].get().strip(),
                  'Tanggal Register': item.css('tr')[6].xpath('.//td/text()')[1].get().strip(),
                  'Lembaga Peradilan': item.css('tr')[7].xpath('.//td')[1].xpath('.//a/text()').getall(),
                  'Jenis Lembaga Peradilan': item.css('tr')[8].xpath('.//td/text()')[1].get().strip(),
                  'Hakim Ketua': item.css('tr')[9].xpath('.//td/text()')[1].get().strip(),
                  'Hakim Anggota': item.css('tr')[10].xpath('.//td/text()')[1].get().strip(),
                  'Panitera': item.css('tr')[11].xpath('.//td/text()')[1].get().strip(),
                  'Amar': item.css('tr')[12].xpath('.//td/text()')[1].get().strip(),
                  'Amar Lainnya': item.css('tr')[13].xpath('.//td/text()')[1].get().strip(),
                  'Catatan Amar': item.css('tr')[14].xpath('.//td//text()').getall(),
                  'Tanggal Musyawarah': item.css('tr')[15].xpath('.//td/text()')[1].get().strip(),
                  'Tanggal Dibacakan': item.css('tr')[16].xpath('.//td/text()')[1].get().strip(),
                  'Link PDF': tabRight.xpath('.//li[6]/a/@href').get(),
                  #'Kaidah': item.css('tr')[17].xpath('.//td/text()')[1].get().strip(),
                  #'Status': item.css('tr')[18].xpath('.//td/text()')[1].get().strip(),
                  #'Abstrak': item.css('tr')[19].xpath('.//td/text()')[1].get().strip(),
                  }
        #anchors = response.css('ul.pagination').css('li a')
        #yield from response.follow_all(anchors, callback=self.parse)
