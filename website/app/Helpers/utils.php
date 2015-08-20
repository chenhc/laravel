<?php

function getTotalPage($totalCount, $pagesize) {
    $totalPage = floor($totalCount / $pagesize);
    $remain = $totalCount % $pagesize;
    if ($remain)
        $totalPage += 1;
    return $totalPage;
}
