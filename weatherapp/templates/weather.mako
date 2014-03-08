<!DOCTYPE html>
<html>
<head>
	<title>Weather - Coldest Cities</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	
    <!-- bootstrap -->
    <link href="/css/bootstrap/bootstrap.css" rel="stylesheet" />
    <link href="/css/bootstrap/bootstrap-overrides.css" type="text/css" rel="stylesheet" />

    <!-- global styles -->
    <link rel="stylesheet" type="text/css" href="/css/compiled/layout.css" />
        <link rel="stylesheet" type="text/css" href="/css/compiled/elements.css" />
    <link rel="stylesheet" type="text/css" href="/css/compiled/icons.css" />


    <!-- libraries -->
    <script src="http://code.jquery.com/jquery-latest.js"></script>
    <script src="/js/bootstrap.min.js"></script>
    <script src="/js/jquery.dataTables.js"></script>
    <script src="/js/theme.js"></script>
    <script src="/js/handlebars-v1.3.0.js"></script>
    <link href="/css/lib/font-awesome.css" type="text/css" rel="stylesheet" />
    <link href="/css/lib/jquery.dataTables.css" type="text/css" rel="stylesheet" />
    <script type="text/javascript" src="/js/ember.js"></script>
    <script type="text/javascript" src="/js/ember-data.js"></script>
    <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAPzpAxEGmu4Dg69-efCmLZg_iZFpLi6Ig&sensor=false"></script>
    
    
    <!-- this page specific styles -->
    <link rel="stylesheet" href="/css/compiled/datatables.css" type="text/css" media="screen" />

    <!-- open sans font -->
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css' />

    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
</head>
<body>
    <!-- templates -->
    <script type="text/x-handlebars" data-template-name="application">
        <!-- navbar -->
        <header class="navbar navbar-inverse" role="banner">
            <div class="navbar-header">
                <button class="navbar-toggle" type="button" data-toggle="collapse" id="menu-toggler">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="index.html"></a>
            </div>
        </header>
        <!-- end navbar -->

        <!-- sidebar -->
        <div id="sidebar-nav">
            <ul id="dashboard-menu">
                <li>                
                    <a href="/">
                        <i class="icon-home"></i>
                        <span>Coldest Cities</span>
                    </a>
                </li>
            </ul>
        </div>
        <!-- end sidebar -->
        
        {{outlet}}
    </script>
    
    <script type="text/x-handlebars" data-template-name="loading">
        <div class="content">
            <div id="pad-wrapper" class="datatables-page">
                <img src="/img/loading_icon.png" style="margin-left:45%; margin-top:200px;"/>
            </div>
        </div>
    </script>
    <script type="text/x-handlebars" data-template-name="index">
        
        <div class="content">
            <div id="pad-wrapper" class="datatables-page">
                <div id="map-canvas" style="width:100%;height:500px;"/>
            </div>

            <button id="save_button" type="button" class="btn-glow primary btn-finish" {{action "reload"}}>
                Reload
            </button>
            
            <p id="countdown"></p>

            <div id="pad-wrapper" class="datatables-page">
                
                <div class="row">
                    <div class="col-md-12">

                        <table id="weather">
                            <thead>
                                <tr>
                                    <th tabindex="0" rowspan="1" colspan="1">Number
                                    </th>
                                    <th tabindex="0" rowspan="1" colspan="1">City
                                    </th>
                                    <th tabindex="0" rowspan="1" colspan="1">Current Temperature (API)
                                    </th>
                                    <th tabindex="0" rowspan="1" colspan="1">Current Temperature (Scrape)
                                    </th>
                                </tr>
                            </thead>
                            
                            <tfoot>
                                <tr>
                                    <th rowspan="1" colspan="1">Number</th>
                                    <th rowspan="1" colspan="1">City</th>
                                    <th rowspan="1" colspan="1">Current Temperature</th>
                                </tr>
                            </tfoot>
                            <tbody>
                                {{#each weather in this}}
                                    <tr>
                                        <td>{{weather.id}}</td>
                                        <td>{{weather.name}}</td>
                                        <td>{{weather.api_temperature}} Celsius</td>
                                        <td>{{weather.scrape_temperature}} Celsius</td>
                                    </tr>
                                {{/each}}
                            </tbody>
                        </table>

                    </div>
                </div>
            </div>
        </div>
    </script>


    
    <!-- application scripts. -->
    <script type="text/javascript" src="/js/application.js"></script>
    <script type="text/javascript" src="/js/model.js"></script>
    <script type="text/javascript" src="/js/router.js"></script>
</body>
</html>
