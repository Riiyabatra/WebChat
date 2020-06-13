<?php
    //  product name
    $myfile = fopen("/Applications/XAMPP/htdocs/msg.txt", "r") or die("Unable to open file!");
    $product = fgets($myfile);
    fclose($myfile);

    // answer for brand (yes or no)
    $myfile = fopen("/Users/ar-riya.batra/Documents/FinalYearProject/final/answer.txt", "r") or die("Unable to open file!");
    $ans = fgets($myfile);
    fclose($myfile);

    if($ans == "yes"){
        // brand name
        $myfile1 = fopen("/Applications/XAMPP/htdocs/brand.txt", "r") or die("Unable to open file!");
        $brand = ucwords(fgets($myfile1));
        fclose($myfile1);
    }

    //price details (min and max)
    // $myfile2 = fopen("/Applications/XAMPP/htdocs/price.txt", "r") or die("Unable to open file!");
    // $content = fgets($myfile2);
    // $price = explode(" ", $content);
    // fclose($myfile2);

    // // feedback score
    // $myfile3 = fopen("/Applications/XAMPP/htdocs/feedback.txt", "r") or die("Unable to open file!");
    // $feedback = fgets($myfile3);
    // fclose($myfile3);
?>

<?php
error_reporting(0);  // turn on all errors
// error_reporting(E_ALL);  // turn on all errors, warnings and notices for easier debugging
$results = '';
$endpoint = 'https://svcs.ebay.com/services/search/FindingService/v1';  // URL to call
$responseEncoding = 'XML';   // Format of the response
$safeQuery = urlencode ($product);
$site  = 'EBAY-IN';

if($ans == "yes"){
    $apicall = "$endpoint?OPERATION-NAME=findItemsAdvanced"
            . "&SERVICE-VERSION=1.13.0"
            . "&GLOBAL-ID=$site"
            . "&SECURITY-APPNAME=TanveerA-webchatf-PRD-dca7d98ed-7a4fab11" //replace with your app id
            . "&keywords=$safeQuery"
            . "&paginationInput.entriesPerPage=1" //number of products to return
            . "&sortOrder=BestMatch"
            . "&itemFilter(0).name=ListingType" 
            . "&itemFilter(0).value=FixedPrice"
            // . "&itemFilter(1).name=MinPrice"
            // . "&itemFilter(1).value=$price[0]"
            // . "&itemFilter(2).name=MaxPrice"
            // . "&itemFilter(2).value=$price[1]"
            // . "&itemFilter(3).name=FeedbackScoreMin"
            // . "&itemFilter(3).value=$feedback"
            . "&aspectFilter(0).aspectName=Brand"
            . "&aspectFilter(0).aspectValueName=$brand";
}
else {
    $apicall = "$endpoint?OPERATION-NAME=findItemsAdvanced"
            . "&SERVICE-VERSION=1.13.0"
            . "&GLOBAL-ID=$site"
            . "&SECURITY-APPNAME=TanveerA-webchatf-PRD-dca7d98ed-7a4fab11" //replace with your app id
            . "&keywords=$safeQuery"
            . "&paginationInput.entriesPerPage=1" //number of products to return
            . "&sortOrder=BestMatch"
            . "&itemFilter(0).name=ListingType" 
            . "&itemFilter(0).value=FixedPrice";
            // . "&itemFilter(1).name=MinPrice"
            // . "&itemFilter(1).value=$price[0]"
            // . "&itemFilter(2).name=MaxPrice"
            // . "&itemFilter(2).value=$price[1]"
            // . "&itemFilter(3).name=FeedbackScoreMin"
            // . "&itemFilter(3).value=$feedback";
}

// Load the call and capture the document returned by the Finding API
$resp = simplexml_load_file($apicall);

if($resp && $resp->paginationOutput->totalEntries > 0) {
    // $results .= 'Total items : ' . $resp->paginationOutput->totalEntries;
    // If the response was loaded, parse it and build links
    foreach($resp->searchResult->item as $item) {
        // if ($item->galleryURL) {
        //   $picURL = $item->galleryURL;
        // } else {
        //   $picURL = "http://pics.ebaystatic.com/aw/pics/express/icons/iconPlaceholder_96x96.gif"; // if no image cannot be retrieved
        // }
        $link  = $item->viewItemURL; //url of the item
        $title = $item->title;
        $price = sprintf("%01.2f", $item->sellingStatus->convertedCurrentPrice);
        // $ship  = sprintf("%01.2f", $item->shippingInfo->shippingServiceCost);
        // $total = sprintf("%01.2f", ((float)$item->sellingStatus->convertedCurrentPrice));
        $results .= nl2br("title: " . $title . ":total price: " . $price) ;
    }
}
else {
    $results = "no results found";
}
echo $results;
?>