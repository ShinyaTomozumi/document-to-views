<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

/**
 * __comment__
 * NOTE: This class is auto generated by yaml_to_view program.__copyright____author__
 * @version __version__
 */
class __controller_name__ extends Controller
{

    /** @var string $viewId */
    private $viewId = "__view_id__";


    /**
     * __construct / 初期化
     */
    public function __construct()
    {

    }


    /**
     * View
     *
     * @param Request $request__comment_params__
     * @return \Illuminate\Contracts\View\Factory|\Illuminate\View\View
     */
    public function view(Request $request__paths__)
    {
        // Define the parameters to be passed to the View.
        // Viewに渡すパラメータを定義する。
        $arrParam = [
        ];

        // View
        return view('__blade_name__', $arrParam);
    }

}
