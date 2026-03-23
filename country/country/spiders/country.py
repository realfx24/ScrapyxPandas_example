import scrapy
import pandas as pd # 1. Import library pandas

class CountrySpider(scrapy.Spider):
    name = 'country'
    start_urls = ['https://www.scrapethissite.com/pages/simple/']
    
    # 2. Buat list kosong untuk menampung semua baris data
    data_list = []

    def parse(self, response):
        countries = response.css('div.col-md-4.country')

        for country in countries:
            name = country.xpath('normalize-space(.//h3[@class="country-name"])').get()
            capital = country.css('span.country-capital::text').get()
            population = country.css('span.country-population::text').get()
            area = country.css('span.country-area::text').get()

            # 3. Masukkan data kotor ke dalam list penampung
            self.data_list.append({
                'Country': (name or "").strip(),
                'Capital': (capital or "").strip(),
                'Population': (population or "").strip(),
                'Area(km)': (area or "").strip()
            })

    # 4. Fungsi bawaan Scrapy yang otomatis berjalan saat scraping SELESAI
    def close(self, reason):
        # Ubah list menjadi DataFrame (Tabel Pandas)
        df = pd.DataFrame(self.data_list)
        
        # Simpan langsung ke file EXCEL asli (.xlsx) agar otomatis rapi!
        df.to_excel('country.xlsx', index=False)
        print("\n🎉 Berhasil! File 'country.xlsx' telah dibuat! 🎉\n")