import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Article } from '../models/article';
import { DomSanitizer } from '@angular/platform-browser';
import { HomeService } from '../services/home/home.service';
import { VerseService } from '../manager.service';
import { Subscription } from "rxjs";

@Component({
  selector: 'app-list-articles',
  templateUrl: './list-articles.component.html',
  styleUrls: ['./list-articles.component.scss']
})

export class ListArticlesComponent implements OnInit, OnDestroy {

  docID: any;
  docName: string;
  docDate: any;
  data: any = {};
  
  public docProcessed: boolean;
  public Articles: Article[] = [];
  public loading: boolean = false;
  public loadingSubscription: Subscription;

  constructor(private route: ActivatedRoute,
              private domSanitizer: DomSanitizer,
              private verseService: VerseService,
              private homeService: HomeService
             ) {
    this.route.queryParams.subscribe(params => {
      this.docName = params['name'];
      this.docDate = params['date'];
      this.docProcessed = params['processed'];
      this.docID = this.route.snapshot.paramMap.get('doc_id');
    });
  }

  ngOnInit() {
    this.loadingSubscription = this.homeService.loadingStatus.subscribe((value) => {
      this.loading = value;
    });
    this.verseService.getArticlesByDocumentId(this.docID).subscribe(objs => {
      this.Articles = objs;
    });
  }

  ngOnDestroy() {
    this.loadingSubscription.unsubscribe();
  }

  sanitize(url: string) {
    return this.domSanitizer.bypassSecurityTrustUrl(url);
  }
}
