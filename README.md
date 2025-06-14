# Special Object Maker

A Blender addon to create special primitives (spindle, capsule, torus, pyramid, gear, star) at the 3D cursor.

## Features

* **Spindle**: Create a double-cone (spindle) with adjustable radius, height, and segments.
* **Capsule**: Create a capsule (cylinder with hemispherical ends) with adjustable radius, height, segments, and hemisphere segments.
* **Torus**: Create a torus (donut) with adjustable major/minor radius and segment counts.
* **Pyramid**: Create a square pyramid with adjustable base size and height.
* **Gear**: Create a simple spur gear with adjustable teeth count, inner/outer radius, and depth.
* **Star**: Create a star-shaped prism with adjustable point count, inner/outer radius, and depth.

## Installation

1. Download or clone this repository.
2. Place `special_object_maker.py` in your Blender addons folder:

   * **Windows**: `%APPDATA%\Blender Foundation\Blender\<version>\scripts\addons\`
   * **macOS / Linux**: `~/.config/blender/<version>/scripts/addons/`
3. In Blender: **Edit > Preferences > Add-ons**, click **Install...** or locate **Special Object Maker** in the list and enable it.

## Usage

1. Open the **3D Viewport** and switch to the **Sidebar (N)**.
2. Find the **Special Objects** tab.
3. Expand the desired object section and adjust parameters.
4. Click **Add \<Object>** to place it at the 3D cursor.

## Supported Blender Versions

* Tested on Blender 4.4.0 and later.

## Contributing

Feel free to open issues or submit pull requests on GitHub. Please follow standard Blender addon structure and coding conventions.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

# Special Object Maker（日本語版）

Blenderの3Dカーソル位置に特殊プリミティブ（スピンドル、カプセル、トーラス、ピラミッド、ギア、星型）を作成するアドオン。

## 主な機能

* **Spindle（スピンドル）**: 先端が円錐形の両錐体。半径、高さ、セグメント数を調整可能。
* **Capsule（カプセル）**: 両端に半球を持つシリンダー。半径、高さ、セグメント数、半球セグメント数を調整可能。
* **Torus（トーラス）**: ドーナツ状オブジェクト。大半径、小半径、セグメント数を調整可能。
* **Pyramid（ピラミッド）**: 正方形の底面を持つ四角錐。底面サイズと高さを調整可能。
* **Gear（ギア）**: 歯車形状。歯数、内/外半径、厚みを調整可能。
* **Star（星型）**: 星型柱。頂点数、内/外半径、厚みを調整可能。

## インストール方法

1. 本リポジトリをダウンロードまたはクローン。
2. `special_object_maker.py` をBlenderのアドオンフォルダに配置:

   * **Windows**: `%APPDATA%\Blender Foundation\Blender\<バージョン>\scripts\addons\`
   * **macOS / Linux**: `~/.config/blender/<バージョン>/scripts/addons/`
3. Blenderで **編集 > プリファレンス > アドオン** から **Special Object Maker** を有効化。

## 使用方法

1. 3Dビューのサイドバー（Nキー）を開き、**Special Objects** タブを選択。
2. 作成したいオブジェクトのセクションを展開し、パラメータを調整。
3. **Add <オブジェクト名>** ボタンをクリックして3Dカーソル位置に配置。

## 動作確認済みバージョン

* Blender 4.4.0以降。

## コントリビュート

Issueの提出やプルリクエストを歓迎します。Blenderアドオンの構造とコーディング規約に従ってください。

## ライセンス

MITライセンスのもとで公開しています。詳細は [LICENSE](LICENSE) をご覧ください。

---

> この README は、プログラム作成プロジェクトにおいて ChatGPT によって生成されました。
